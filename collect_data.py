from apiclient.discovery import build
import pandas as pd
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

class CollectMovieData:
    """
    Youtube Data API v3を用いて、検索クエリにマッチする動画の情報を取得する
    delta="year"のみ動作確認済み
    """

    def __init__(self, api_key, years, delta, query=None, channel_id=None, save=False, save_path='output/tmp/'):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.ym_list = [(y,1) for y in range(years[0], years[1]+1)]
        self.delta = delta
        self.query = query
        self.channel_id = channel_id
        self.save = save
        self.save_path = save_path

    def get_responses(self, start_time, end_time, next_token=None):
        """ 検索クエリにマッチするresponseを取得 """
        params = {
            'part': 'snippet', # searchリソースのプロパティを指定 (shippet: 全てのプロパティを取得)
            'type': 'video', # 検索対象のリソースタイプを指定 (channel, playlist, video)
            'regionCode': "jp", # 検索対象の国コード
            'order': "viewCount", # 視聴回数順に取得
            'publishedAfter': start_time, # 検索の開始時間 （例: 1970-01-01T00:00:00Z）
            'publishedBefore': end_time, # 検索の終了時間
            'maxResults': 50
        }
        if next_token:
            params['pageToken'] = next_token
        if self.query:  # 検索クエリ
            params['q'] = self.query
        if self.channel_id:  # チャンネルID
            params['channelId'] = self.channel_id
            self.query = self.channel_id # 後々のtitle用
        return self.youtube.search().list(**params).execute()

    def get_items(self, responses):
        """ responsesから必要な情報を取得し、DataFrameに変換する """
        cols = ['title', 'description', 'publishTime', 'channelTitle']
        data = [[item['id']['videoId']] + [item['snippet'][x] for x in cols] for item in responses['items']]
        return pd.DataFrame(data, columns=['video_id'] + cols)

    def get_time(self, start_year, start_month):
        """ 検索の開始時間と終了時間を取得 """
        start_date = datetime(start_year, start_month, 1)
        deltas = {
            'day': relativedelta(days=1),
            '10days': relativedelta(days=10),
            'month': relativedelta(months=1),
            'year': relativedelta(years=1)
        }
        end_date = start_date + deltas[self.delta]
        return start_date.isoformat() + 'Z', end_date.isoformat() + 'Z'

    def get_all_df_multi(self, start_year, start_month):
        """ 複数期間のデータを結合 """
        start_time, end_time = self.get_time(start_year, start_month)
        df_list = []
        next_token = None
        while True:
            response = self.get_responses(start_time, end_time, next_token)
            df_list.append(self.get_items(response))
            next_token = response.get('nextPageToken')
            if not next_token:
                break
        all_df = pd.concat(df_list, axis=0).drop_duplicates(subset='video_id').reset_index(drop=True)
        title = f"{self.query}_{start_year}_{start_month}.csv"
        print(f"{title}, shape:{all_df.shape}, response_count:{len(df_list)}")
        if self.save:
            all_df.to_csv(f'{self.save_path}/{title}', index=False)
            print(title, all_df.shape)
        return all_df

    def run(self):
        for year, month in tqdm(self.ym_list):
            df = self.get_all_df_multi(year, month)
        return df

class CollectCommentData:
    """
    Youtube Data API v3を用いて、検索クエリにマッチする動画のコメントの情報を取得する
    """
    def __init__(self, api_key, video_id_list, save=False, save_path='output/tmp/', title="comment", save_number=1):
        """ 初期化 """
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.video_id_list = video_id_list
        self.save = save
        self.save_path = save_path
        self.title = title
        self.save_number = save_number
        self.rename_dict = {
            "textDisplay":"comment",
            "likeCount":"likes",
            "publishedAt": "publish_time",
            "authorChannelId":"author_id",
        }

    def get_responses(self, video_id, next_token=None):
        """ 検索クエリにマッチするresponseを取得 """
        params = {
            'part': 'snippet',
            'videoId': video_id,
            'textFormat': 'plainText',
            'order': 'time',
            'maxResults': 100
        }
        if next_token:
            params['pageToken'] = next_token
        return self.youtube.commentThreads().list(**params).execute()

    def get_items(self, responses):
        """ responsesから必要な情報を取得し、DataFrameに変換する """
        cols = ['textDisplay', 'likeCount', 'publishedAt']
        all_data = []
        for item in responses['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            data = [snippet.get(c, None) for c in cols] + [snippet['authorChannelId']['value']]
            all_data.append(data)
        return pd.DataFrame(all_data, columns=cols+['authorChannelId'])

    def get_all_comments(self, video_id):
        """ 指定した動画IDのすべてのコメント情報を取得 """
        next_token = None
        df_list = []
        while True:
            responses = self.get_responses(video_id, next_token)
            df_list.append(self.get_items(responses))
            next_token = responses.get('nextPageToken')
            if next_token is None:
                break
        all_df = pd.concat(df_list, axis=0).reset_index(drop=True)
        all_df["video_id"] = video_id
        print(video_id, all_df.shape)
        return all_df

    def save_check(self, final=False):
        """ 一定数(300)ごとにデータを保存 """

        if self.save:
            if (self.count > 300) or (final and self.count>0):
                self.df = pd.concat(self.all_df_list, axis=0).rename(columns=self.rename_dict)
                title = f"{self.title}_{str(self.save_number).zfill(2)}.csv"
                self.df.to_csv(f'{self.save_path}/{title}', index=False)
                print('save:', title, self.df.shape)

                self.count = 0
                self.all_df_list = []
                self.save_number += 1
        elif final:
            self.df = pd.concat(self.all_df_list, axis=0).rename(columns=self.rename_dict)

    def run(self):
        self.all_df_list = []
        self.count = 0
        for video_id in tqdm(self.video_id_list):
            try:
                all_df = self.get_all_comments(video_id)
                self.all_df_list.append(all_df)
                self.count += len(all_df)
                self.save_check()
            except:
                print("collect error: ", video_id)
        self.save_check(final=True)
        if not self.save:
            return self.df

class CollectMovieStatsData(CollectMovieData):
    """
    Youtube Data API v3を用いて、検索クエリにマッチする動画の統計情報を取得する
    """
    def __init__(self, api_key,video_id_list, save=False, save_path='output/tmp/'):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.video_id_list = video_id_list
        self.save = save
        self.save_path = save_path

    def get_video_details(self, video_id):
        """
        video_idを使用して、動画の視聴回数、いいね数、低評価数、コメント数を取得します
        """
        # YouTube Data API v3のvideosリソースを使用して、動画の詳細情報を取得
        response = self.youtube.videos().list(
            part="statistics", # 動画の統計情報を取得するために使用
            id=video_id # 詳細情報を取得する動画のID
        ).execute()

        # 必要な情報を取得
        stats = response["items"][0]["statistics"]
        return {
            "videoId": video_id,
            "viewCount": stats.get("viewCount", 0),
            "likeCount": stats.get("likeCount", 0),
            "dislikeCount": stats.get("dislikeCount", 0),
            "commentCount": stats.get("commentCount", 0)
        }

    def get_video_details_for_list(self, video_ids_list):
        """
        video_ids_listを使用して、各動画の視聴回数、いいね数、低評価数、コメント数を取得し、pd.DataFrameで出力します
        """
        # 各動画IDの詳細情報をリストとして収集
        details_list = [self.get_video_details(video_id) for video_id in video_ids_list]

        # リストをpd.DataFrameに変換
        df = pd.DataFrame(details_list)
        return df

    def run(self):
        df = self.get_video_details_for_list(self.video_id_list)
        if self.save:
            df.to_csv(f'{self.save_path}/stats.csv', index=False)
        return df

class YouTubeDataCollector:
    def __init__(self, api_key, mode, args):
        """
        api_key: APIキー
        mode: 動画、コメントなどのモードを指定 (e.g., 'movie', 'comment', 'stats')
        args: それぞれのモードに合わせて指定する引数を辞書形式で
        """
        self.api_key = api_key
        self.mode = mode
        self.args = args
        self.collector = self._get_collector()

    def _get_collector(self):
        # モードに応じて、対応するクラスをインスタンス化する
        if self.mode == 'movie':
            return CollectMovieData(self.api_key, **self.args)
        elif self.mode == 'comment':
            return CollectCommentData(self.api_key, **self.args)
        elif self.mode == 'stats':
            return CollectMovieStatsData(self.api_key, **self.args)
        else:
            raise ValueError('Invalid mode!')

    def run(self):
        # 実行
        return self.collector.run()

    def read_all_df(path, show_names=False):
        """ フォルダ内の全てのcsvを読み込み、結合する"""
        names = sorted(os.listdir(path))
        print('\n'.join(names))
        all_df = pd.concat([pd.read_csv(path / name) for name in names], axis=0)
        # publisht_timeがあるかどうか
        if 'publishTime' in all_df.columns:
            all_df = all_df.drop_duplicates(subset='video_id').sort_values('publishTime')
        all_df = all_df.reset_index(drop=True)
        print("all shape:", all_df.shape)
        return all_df
    
    def pickup_video_id(df):
        """video_idのみのデータを作成"""
        video_id_list = df['video_id'].unique().tolist()
        print('video_id:', len(video_id_list))
        return video_id_list

if __name__ == '__main__':
    YOUTUBE_API_KEY = 'AAAAAAAAAAAAAA'

    # movie の場合
    collector = YouTubeDataCollector(
        api_key=YOUTUBE_API_KEY,
        mode='movie',  # 'comment', 'stats' も利用可能
        args = {
            'years': (2018, 2020),
            'delta': 'year',
            'query': 'キーワード OR keyword',
            'save': False
        }
    )
    collector.run()
