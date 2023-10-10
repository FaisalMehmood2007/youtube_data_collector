# youtube_data_collector

YouTube API v3を用いて、キーワードやチャンネル名を指定して、動画のメタデータ、統計データ、コメント等を収集するためのコードになります。  
2023.10.10 現在説明を編集中ですが、コード自体は動作する状態です。(ただし今後アップデートする可能性あり)

## コードの前の準備
1. Google Cloud PlatformでYouTube API　v3 のAPIキーを取得してください。[(参考サイト)](https://qiita.com/shinkai_/items/10a400c25de270cb02e4)
2. このライブラリをインポートします。
   ```
   !git clone https://github.com/momijiro/youtube_data_collector
   from youtube_data_collector.collect_data import YouTubeDataCollector
   ```
3. キーワード・チャンネル名を指定し動画データ(タイトル、概要、video_id等）を収集します。  
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
 4. 動画データを元に、コメント、動画の統計を収集します。
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
    
    (b) 動画の統計(いいね数、視聴数等)
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

   動作しない点・不明点等がありましたら、ご連絡ください。(https://twitter.com/kanure24)
   また、Fork・Star等くださると嬉しいです。
