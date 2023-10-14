## `youtube_data_collector`: YouTubeデータの収集コード

[YouTube API v3](https://developers.google.com/youtube/v3/docs?hl=ja)を活用し、YouTubeデータの収集を行うコードになります。  
APIの機能はかなり広いため、このコードでは以下の機能に限定しています。

## 主な機能

1. **動画メタデータの抽出**  
  (a) 指定したキーワードの動画の収集  
  (b) 指定したチャンネル名の動画の収集
2. **`video_id` を用いた詳細情報の取得**  
  (a) コメントの収集  
  (b) 統計の収集（いいね数、視聴数など）

## 収集の前に
1. Google Cloud Platform で YouTube API v3 のキーを取得します。[(こちらの記事が参考になります。)](https://qiita.com/shinkai_/items/10a400c25de270cb02e4)
2. このライブラリをインポートします。
   ```bash
   !git clone https://github.com/momijiro/youtube_data_collector
   from youtube_data_collector.collect_data import YouTubeDataCollector
   ```

## 実行

### 1. 動画メタデータの収集

  (a) キーワードを指定
  ```python
  YOUTUBE_API_KEY = 'YOUR_API_KEY'  # 自分の API キーに置き換えてください。
  collector = YouTubeDataCollector(
     api_key=YOUTUBE_API_KEY,
     mode='movie',
     args={
           'query': '<キーワード>',
           'start': 'YYYY',
           'end': 'YYYY',
           'save': True,
           'save_path': './'
     }
  )
  final_df = collector.run()  # 最終的なデータフレームのみが保存されます。
  ```

  (b) チャンネル名を指定 
  ```python
  collector = YouTubeDataCollector(
     api_key=YOUTUBE_API_KEY,
     mode='movie',
     args={
           'channel_id': '<チャンネルID>',
           'start': 'YYYY',
           'end': 'YYYY',
           'save': True,
           'save_path': './'
     }
  )
  final_df = collector.run()  # 最終的なデータフレームのみが保存されます。
  ```

### 2. `video_id` を用いた詳細情報の取得

  ```python
  # video_id_list を取得
  path = './'
  all_df = collector.read_all_df(path)
  video_id_list = collector.pickup_video_id(all_df)
  ```

  (a) コメントの収集
  ```python
  collector_comment = YouTubeDataCollector(
     api_key=YOUTUBE_API_KEY,
     mode='comment',
     args={
           'video_id_list': video_id_list,
           'save_threshold': 500,
           'save': False,
           'save_path': '<保存先パス>',
           'title': 'mid_comment',
           'save_number': 0
     }
  )
  final_df = collector_comment.run()  # 最終的なデータフレームのみが保存されます。
  ```

  (b) 統計情報の収集  
  ```python
  collector_stats = YouTubeDataCollector(
     api_key=YOUTUBE_API_KEY,
     mode='stats',
     args={
           'video_id_list': video_id_list,
           'save': True,
           'save_path': './'
     }
  )
  final_df = collector_stats.run()  # 最終的なデータフレームのみが保存されます。
  ```

---

問題・不明点等ありましたら、お気軽にお問い合わせください。  
このコードが役に立ちましたらStarをいただけると幸いです！
連絡先: [X(Twitter)](https://twitter.com/kanure24) 

---
