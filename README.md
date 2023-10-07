# youtube_data_collector

YouTube API v3を用いて、キーワードやチャンネル名を指定して、動画のメタデータ、統計データ、コメント等を収集するた目のコードになります。

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
   YOUTUBE_API_KEY = 'YOUR_API_KEY',
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
