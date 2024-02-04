from youtube_analytics_api_functions import YoutubeAnalyticsData
from youtube_data_api_functions import YoutubeChannelData
from datetime import datetime

CHANNEL_ID = 'UCAFhdtRnKRqJQI7ht1Puo9Q'

if __name__ == '__main__':

    youtube_data = YoutubeChannelData()
    youtube_analytics = YoutubeAnalyticsData()

    videos_basic_info = youtube_data.get_channel_videos_basic_info(CHANNEL_ID)
    
    for video_basic_info in videos_basic_info:
        video_stats = youtube_analytics.get_video_analytics(video_basic_info)
        print(video_stats)