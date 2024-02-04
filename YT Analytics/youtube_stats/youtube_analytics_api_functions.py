from get_service import youtube_analytics_service
from tabulate import tabulate
from datetime import datetime
import csv

class YoutubeAnalyticsData:
    
    def __init__(self):
        self.YOUTUBE_SERVICE = youtube_analytics_service()

    def execute_api_request(self, client_library_function, **kwargs):
        response = client_library_function(**kwargs).execute()
        return response

    def video_views_day_by_day(self, video_id, startDate, endDate):
        result = self.execute_api_request(
            self.YOUTUBE_SERVICE.reports().query,
            ids='channel==MINE',
            startDate=startDate,
            endDate=endDate,
            metrics='views',
            dimensions='day',
            sort='day',
            filters=f'video=={video_id}'  # Filters for the specific video ID
        )

        return result

    def get_video_analytics(self, basic_video_info):

        analytics_data = []
        end_date = datetime.utcnow().strftime('%Y-%m-%d')  # Current date in YYYY-MM-DD format
        start_date = datetime.strptime(basic_video_info['Video Publication Time'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")

        metrics = 'views,likes,dislikes,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost'
        dimensions = 'video'
        
        video_id = basic_video_info['Content']  # Assuming 'Content' holds the video ID
        print(video_id)
        results = self.execute_api_request(
            self.YOUTUBE_SERVICE.reports().query,
            ids='channel==MINE',
            startDate=start_date,
            endDate=end_date,
            metrics=metrics,
            dimensions=dimensions,
            filters=f'video=={video_id}'
        )

        if results.get('rows', []):
            data = results['rows'][0]
            analytics = {
                'Video ID': video_id,
                'Views': data[0],
                'Likes': data[1],
                'Dislikes': data[2],
                'Estimated Watch Time (minutes)': data[3],
                'Average View Duration': data[4],
                'Subscribers Gained': data[5],
                'Subscribers Lost': data[6]
            }
            analytics_data.append(analytics)
        else:
            analytics_data.append({'Video ID': video_id, 'Error': 'No data available'})

        return analytics_data