from apiclient.discovery import build
import pandas as pd
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

class CollectMovieData:
    """
    Youtube Data API v3を用いて、検索クエリにマッチする動画の情報を取得する
    """

    def __init__(self, api_key, start, end, query=None, channel_id=None, save=False, save_path='output/tmp/'):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.query = query
        self.channel_id = channel_id
        self.save = save
        self.save_path = save_path
        self.date_list = self._get_date_list(start, end)  # deltaとdate_listを同時に返すように変更

    def _get_date_list(self, start, end):
        """ start, end の形式から delta を決定 """
        n = len(start)
        assert n == len(end), 'Invalid date format for start or end.'

        if n == 4:
            self.delta = 'year'
            start_date = datetime.strptime(start, '%Y') # yaer -> 1/1を取得
            end_date = datetime.strptime(end, '%Y') + relativedelta(years=1) - timedelta(days=1) # year -> 12/31を取得
            return self._generate_date_list(start_date, end_date)
        elif n == 7:
            self.delta = 'month'
            start_date = datetime.strptime(start, '%Y-%m') # year-month -> 1/1を取得
            end_date = datetime.strptime(end, '%Y-%m') + relativedelta(months=1) - timedelta(days=1) # year-month -> 月末を取得
            return self._generate_date_list(start_date, end_date)
        elif n == 10:
            self.delta = 'day'
            start_date = datetime.strptime(start, '%Y-%m-%d')
            end_date = datetime.strptime(end, '%Y-%m-%d')
            return self._generate_date_list(start_date, end_date)
        else:
            raise ValueError('Invalid date format for start or end.')

    def _generate_date_list(self, start_date, end_date):
        """ deltaに応じた日付リストを生成 """
        deltas = {
            'day': relativedelta(days=1),
            'month': relativedelta(months=1),
            'year': relativedelta(years=1)
        }
        current_date = start_date
        date_list = []
        while current_date <= end_date:
            date_list.append(current_date)
            current_date += deltas[self.delta]
        return date_list

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

    def get_time(self, current_date):
        """ 検索の開始時間と終了時間を取得 """
        deltas = {
            'day': relativedelta(days=1),
            'month': relativedelta(months=1),
            'year': relativedelta(years=1)
        }
        end_date = current_date + deltas[self.delta]
        return current_date.isoformat() + 'Z', end_date.isoformat() + 'Z'

    def get_all_df_multi(self, current_date):
        """ 複数期間のデータを結合 """
        start_time, end_time = self.get_time(current_date)
        df_list = []
        next_token = None
        while True:
            response = self.get_responses(start_time, end_time, next_token)
            df_list.append(self.get_items(response))
            next_token = response.get('nextPageToken')
            if not next_token:
                break
        all_df = pd.concat(df_list, axis=0).drop_duplicates(subset='video_id').sort_values('publishTime').reset_index(drop=True)
        def to_str(x):
            return str(x).zfill(2)
        if self.delta == 'year':
            text = f"{current_date.year}"
        elif self.delta == 'month':
            text = f"{current_date.year}_{to_str(current_date.month)}"
        elif self.delta == 'day':
            text = f"{current_date.year}_{to_str(current_date.month)}_{to_str(current_date.day)}"
        title = f"{self.query}_{text}.csv"
        print(f"{title}, shape:{all_df.shape}, response_count:{len(df_list)}")
        if self.save:
            all_df.to_csv(f'{self.save_path}/{title}', index=False)
            print(title, all_df.shape)
        return all_df

    def run(self):
        for current_date in tqdm(self.date_list):
            df = self.get_all_df_multi(current_date)
        return df

class CollectCommentData:
    """
    Youtube Data API v3を用いて、検索クエリにマッチする動画のコメントの情報を取得する
    """
    def __init__(self,
                api_key,
                video_id_list,
                save_threshold=300,
                save=False,
                save_path='output/tmp/',
                title='comment',
                save_number=1):
        """_summary_

        Args:
            api_key (str): 自分のAPIキーを入力
            video_id_list (list): 動画IDのリスト
            save_threshold (int): 一定数ごとにデータを保存するかの閾値 (default: データ数が300以上の場合に保存)
            save (bool): データを保存するかどうか
            save_path (str): 保存先のパス
            title (str): 保存するファイル名
            save_number (int): 保存するファイル名の番号 (default: 1)
        """
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.video_id_list = video_id_list
        self.save_threshold = save_threshold
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
        """ 一定数ごとにデータを保存 """
        if self.save:
            if (self.count > self.save_threshold) or (final and self.count>0):
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
            except Exception as e:
                # YouTube APIの過剰使用エラーの場合のエラーメッセージを確認する
                # ここでは'quotaExceeded'という文字列を仮に使用しています
                if 'Quota' in str(e):
                    print("YouTube APIの使用量が上限に達しました。ビデオID: ", video_id)
                    break  # ループからの脱出（実行中断）
                else:
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
        try:
            stats = response["items"][0]["statistics"]
            return {
                "videoId": video_id,
                "viewCount": stats.get("viewCount", 0),
                "likeCount": stats.get("likeCount", 0),
                "dislikeCount": stats.get("dislikeCount", 0),
                "commentCount": stats.get("commentCount", 0)
            }
        except Exception as e:
            print(f"Error: {video_id} {e}")
            return {
                "videoId": video_id,
                "viewCount": 0,
                "likeCount": 0,
                "dislikeCount": 0,
                "commentCount": 0
            }

    def get_video_details_for_list(self, video_id_list):
        """
        video_id_listを使用して、各動画の視聴回数、いいね数、低評価数、コメント数を取得し、pd.DataFrameで出力します
        """
        # 各動画IDの詳細情報をリストとして収集
        details_list = [self.get_video_details(video_id) for video_id in video_id_list]

        # リストをpd.DataFrameに変換
        df = pd.DataFrame(details_list)
        return df

    def run(self):
        # try:
        df = self.get_video_details_for_list(self.video_id_list)
        # except Exception as e:
        #     print(e)
            # return None
        if self.save:
            df.to_csv(f'{self.save_path}/movie_stats.csv', index=False)
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

    # 収集後に実行
    def read_all_df(self, path, show_names=False):
        """ 指定したパスの(全ての)csvを読み込み、結合する"""
        if str(path).split(".")[-1] == "csv":
            print(path)
            all_df = pd.read_csv(path)
        else:
            names = sorted(os.listdir(path))
            print('\n'.join(names))
            all_df = pd.concat([pd.read_csv(path / name) for name in names], axis=0)
        # publisht_timeがあるかどうか
        if 'publishTime' in all_df.columns:
            all_df = all_df.drop_duplicates(subset='video_id').sort_values('publishTime')
        all_df = all_df.reset_index(drop=True)
        print("all shape:", all_df.shape)
        return all_df

    def pickup_video_id(self, df):
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
