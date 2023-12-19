# `youtube_data_collector`: YouTube Data Collection Code

This code utilizes the [YouTube API v3](https://developers.google.com/youtube/v3/docs) to collect YouTube data. While the API offers a wide range of functionalities, this code focuses on specific features.

## Main Features

1. **Extracting Video Metadata**
   - Collecting videos based on specified keywords
   - Collecting videos based on specified channel names
2. **Obtaining Detailed Information Using `video_id`**
   - Collecting comments
   - Collecting statistical data (e.g., likes, views)

## Quick Start
1. Obtain your YouTube API key from the [Google Cloud Console](https://console.cloud.google.com/).

2. Execute the following code to collect data.
   ```python
   # Importing the library
   !git clone https://github.com/momijiro/youtube_data_collector
   from ytdc import YouTubeDataCollector

   YOUTUBE_API_KEY = 'YOUR_API_KEY'  # Replace with your API key
   collector = YouTubeDataCollector(
      api_key=YOUTUBE_API_KEY,
      mode='movie',
      args={
            'query': 'Christmas',
            'start': '2010-12',
            'end': '2010-12',
      }
   )
   final_df = collector.run()  # Save the final dataframe
   final_df

---

If you have any questions or issues, feel free to contact us.  
If you find this code helpful, we'd appreciate a Star!  
Contact: [X(Twitter)](https://twitter.com/kanure24)

---

# `youtube_data_collector`: YouTubeデータの収集コード

こちらは、[YouTube API v3](https://developers.google.com/youtube/v3/docs?hl=ja)を活用し、YouTubeデータの収集を行うコードになります。  
APIの機能はかなり広いため、このコードでは以下の機能に限定しています。

## 主な機能

1. **動画メタデータの抽出**  
  (a) 指定したキーワードの動画の収集  
  (b) 指定したチャンネル名の動画の収集
2. **`video_id` を用いた詳細情報の取得**  
  (a) コメントの収集  
  (b) 統計の収集（いいね数、視聴数など）

## Quick Start
1. 自分の YouTube API キーを取得してください。API キーは [Google Cloud Console](https://console.cloud.google.com/) から取得できます。

2. 下記のコードを実行することで、簡単にデータが収集できます。
```python
# ライブラリをインポート
!git clone https://github.com/momijiro/youtube_data_collector
from ytdc import YouTubeDataCollector

YOUTUBE_API_KEY = 'YOUR_API_KEY'  # 自分の API キーに置き換えてください
collector = YouTubeDataCollector(
   api_key=YOUTUBE_API_KEY,
   mode='movie',
   args={
         'query': 'クリスマス',
         'start': '2010-12',
         'end': '2010-12',
   }
)
final_df = collector.run()  # 最終的なデータフレームのみ保存
final_df
```

## より詳しい使い方について
詳細な使用方法については、以下のドキュメントを参照してください。

- quick start
- 主な機能について
- 詳しい使い方
- 実用に向けて

---

問題・不明点等ありましたら、お気軽にお問い合わせください。  
このコードが役に立ちましたらStarをいただけると幸いです！  
連絡先: [X(Twitter)](https://twitter.com/kanure24) 

---
