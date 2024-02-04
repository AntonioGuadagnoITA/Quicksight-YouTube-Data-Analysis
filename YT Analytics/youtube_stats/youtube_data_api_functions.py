from get_service import youtube_data_service

class YoutubeChannelData:
    
    def __init__(self):
        self.YOUTUBE_SERVICE = youtube_data_service()

    # Return all information for all videos. 
    #
    # {
    #     "kind",
    #     "etag",
    #     "id",
    #     "snippet":{
    #         "publishedAt",
    #         "channelId",
    #         "title",
    #         "description",
    #         "thumbnails":{
    #             "default":{
    #                 "url",
    #                 "width",
    #                 "height"
    #             },
    #             "medium":{
    #                 "url",
    #                 "width",
    #                 "height"
    #             },
    #             "high":{
    #                 "url",
    #                 "width",
    #                 "height"
    #             },
    #             "standard":{
    #                 "url",
    #                 "width",
    #                 "height"
    #             },
    #             "maxres":{
    #                 "url",
    #                 "width",
    #                 "height"
    #             }
    #         },
    #         "channelTitle",
    #         "tags":,
    #         "categoryId",
    #         "liveBroadcastContent",
    #         "defaultLanguage",
    #         "localized":{
    #             "title",
    #             "description"
    #         },
    #         "defaultAudioLanguage"
    #     }
    # }
    
    def get_channel_videos_info(self, channel_id):
        # Get the Uploads playlist ID
        request = self.YOUTUBE_SERVICE.channels().list(part='contentDetails', id=channel_id)
        response = request.execute()
        playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        videos = []
        next_page_token = None

        # Retrieve all videos from the Uploads playlist
        while True:
            pl_request = self.YOUTUBE_SERVICE.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            pl_response = pl_request.execute()

            video_ids = [item['snippet']['resourceId']['videoId'] for item in pl_response['items']]
            videos_info_request = self.YOUTUBE_SERVICE.videos().list(
                part='snippet',
                id=','.join(video_ids)
            )
            videos_info_response = videos_info_request.execute()

            for video_info in videos_info_response['items']:
                videos.append(video_info)

            next_page_token = pl_response.get('nextPageToken')

            if not next_page_token:
                break

        return videos

    # Return basic information for all videos. 
    # For each video returns: [title, id, published_at]
    def get_channel_videos_basic_info(self, channel_id):

        basic_videos_info = []
        videos = self.get_channel_videos_info(channel_id)

        for video in videos:
            info = {
                'Content': video['id'],
                'Video Title': video['snippet']['title'],
                'Video Publication Time': video['snippet']['publishedAt']
            }
            basic_videos_info.append(info)

        return basic_videos_info