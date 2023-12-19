# 使用方法

このガイドでは、`youtube_data_collector` ライブラリを使用して YouTube のデータを収集する方法を説明します。

1. 自分の YouTube API キーを取得してください。API キーは [Google Cloud Console](https://console.cloud.google.com/) から取得できます。

2. 下記のコードを実行することで、簡単にデータが収集できます。この例では、2010年12月の「クリスマス」に関連するデータを収集します。（本トライアルにおけるAPI の無駄遣いを避けるために、2010年としています）

```python
# ライブラリをインポート (自動で使用するライブラリをインポート)
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

