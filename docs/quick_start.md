# Usage

This guide explains how to use the `youtube_data_collector` library to collect data from YouTube.

1. Prepare your YouTube API key. You can obtain an API key from the [Google Cloud Console](https://console.cloud.google.com/).

2. You can easily collect data by running the code below. In this example, we will collect data related to "Christmas" in December 2010. (The year 2010 is used to avoid wasting the API in this trial.)

```python
# Import the library (Automatically import the libraries to be used)
!git clone https://github.com/momijiro/youtube_data_collector
from ytdc import YouTubeDataCollector

YOUTUBE_API_KEY = 'YOUR_API_KEY'  # Replace with your own API key
collector = YouTubeDataCollector(
   api_key=YOUTUBE_API_KEY,
   mode='movie',
   args={
         'query': 'Christmas',
         'start': '2010-12',
         'end': '2010-12',
   }
)
final_df = collector.run()  # Save only the final dataframe
final_df
```