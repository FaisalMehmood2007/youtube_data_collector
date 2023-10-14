# youtube_data_collector
2023.10.14 現在説明を編集中ですが、コード自体は動作する状態です。(ただし今後アップデートする可能性あり)

[YouTube API v3](https://developers.google.com/youtube/v3/docs?hl=ja)を用いて、YouTube上のデータを収集するコードになります。  
YouTube API v3には様々な機能がありますが、本コードの対応範囲は以下で、自身の動画の統計情報等の収集は対象外となります。
- (1) 動画データ(タイトル、概要、video_id等)の収集
   - (a) 指定したキーワードの動画を収集
   - (b) 指定したチャンネルの動画を収集
- (2) video_idを元に、その動画の詳細情報の収集
   - (a) その動画のコメントを収集
   - (b) その動画の統計(いいね数、視聴数等)を取得

詳しい実行方法・結果は記事を参考にしてください。

## 収集前の準備
1. Google Cloud PlatformでYouTube API v3 のAPIキーを取得してください。[(こちらの記事が参考になります。)](https://qiita.com/shinkai_/items/10a400c25de270cb02e4)
2. このライブラリをインポートします。
   ```
   !git clone https://github.com/momijiro/youtube_data_collector
   from youtube_data_collector.collect_data import YouTubeDataCollector
   ```
## 指定したデータの収集
1. 動画データ(タイトル、概要、video_id等)の収集  
   (a) キーワードを指定  
   ```
   YOUTUBE_API_KEY = 'YOUR_API_KEY', # あなたのYouTube APIキーを入力してください。
   collector = YouTubeDataCollector(
      api_key=YOUTUBE_API_KEY,
      mode='movie', # comment, stats
      args = {
            'query': 'キーワード',
            'start': '2013',
            'end' : '2013',
            'save': True,
            'save_path': './'
      }
      )
   # 最終的なデータのみが保存される
   final_df = collector.run()
   ```
   (b) チャンネル名を指定  
   ```
   collector = YouTubeDataCollector(
   api_key = cfg.YOUTUBE_API_KEY,
      mode = 'movie',
      args = {
         'channel_id': 'SpecifyYouTubeChanelID',
         'start': '2013',
         'end' : '2013',
         'save': True,
         'save_path': './'
      }
   )
   # 最終的なデータのみが保存される
   final_df = collector.run()
   ```

2. video_idを元に、その動画の詳細情報の収集  
   ```
   # video_id_listを取得
   path = './' # save_pathもしくはファイル名を指定
   all_df = collector.read_all_df(path)
   video_id_list = collector.pickup_video_id(all_df)
   ```
   (a) コメントを収集  
   ```
   collector_comment = YouTubeDataCollector(
         api_key = YOUTUBE_API_KEY,
         mode = 'comment',
         args = {
               'video_id_list': video_id_list,
               'save_threshold': 500,
               'save': False,
               'save_path': cfg.output_path / 'mid_comment',
               'title': 'mid_comment',
               'save_number': 0
         }
      )
   # 最終的なデータのみが保存される
   final_df = collector_comment.run()
   ```

   (b) 動画の統計(いいね数、視聴数等)を収集  
   ```
   collector_stats = YouTubeDataCollector(
         api_key = YOUTUBE_API_KEY,
         mode = 'stats',
         args = {
               'video_id_list': video_id_list,
               'save': True,
               'save_path': './'
         }
   )
   # 最終的なデータのみが保存される
   final_df = collector_stats.run()
   ```

動作しない点・不明点等がありましたら、ご連絡ください。  
もし良かったらStar等くださると幸いです！  
連絡先: [X(Twitter)](https://twitter.com/kanure24) 

--- 


