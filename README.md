# `youtube_data_collector`

This code utilizes the [YouTube API v3](https://developers.google.com/youtube/v3/docs) to collect YouTube data. While the API offers a wide range of functionalities, this code focuses on specific features.

## Main Features

1. **Extracting Video Metadata**
   - Collecting videos based on specified keywords
   - Collecting videos based on specified channel names
2. **Obtaining Detailed Information Using `video_id`**
   - Collecting comments
   - Collecting Video statistics (e.g., likes, views)

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


# (日本語版)

こちらは、[YouTube API v3](https://developers.google.com/youtube/v3/docs?hl=ja)を活用し、YouTubeデータの収集を行うコードになります。  
YouTube APIの機能は広いですが、本コードの収集対象は以下の3つに絞っています。
- **動画のメタデータ**：タイトル、概要など
- **動画のコメント**
- **動画の統計データ**：いいね数、視聴数など


## Quick Start

最短でYouTubeデータの収集までを実行できる手順を説明します。

1. [Google Cloud Console](https://console.cloud.google.com/)で、YouTube APIキーを取得します。(詳しくはブログの記事をご覧ください。)

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
   final_df = collector.run()  # 最終月のデータのみ保持
   final_df
   ```
   ※ 直近データではquotaを多く消費してしまうため、2010年としています。

   #### 結果のイメージ (※実データではありません)
   | video_id   | title   | description   | publishTime   | channelTitle   |
   |------------|---------|-------------|------------|----------------|
   |ab12cd|クリスマスパーティ|友達と家でパーティ！|2010-12-21T01:23:45Z|Helloworld|
   |zy34xw|今日はクリスマス！|ついに今年もクリスマスになりました。|2010-12-25T04:56:00Z|Dummies|

## より詳しい使い方について
詳細な使用方法については、以下のドキュメントを参照してください。

- 主な機能について (動画・コメント・統計の収集)
- 詳しい使い方 (細かい設定方法など)
- 実用に向けて (APIやquotaに関する説明)


---
If you have any questions or issues, feel free to contact us.  
If you find this code helpful, we'd appreciate a Star!  

問題・不明点等ありましたら、お気軽にお問い合わせください。  
このコードが役に立ちましたらStarをいただけると幸いです！  

連絡先: [X(Twitter)](https://twitter.com/kanure24) 

---
