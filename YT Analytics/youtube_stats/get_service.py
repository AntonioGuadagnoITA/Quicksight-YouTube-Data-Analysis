from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Scope definition for both APIs - 'YouTube Analytics' and 'YouTube Data'
SCOPES = [
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/youtube.readonly'
]

API_SERVICE_NAME_YOUTUBE_ANALYTICS = 'youtubeAnalytics'     # YouTube Analytics API
API_SERVICE_NAME_YOUTUBE_DATA = 'youtube'                   # YouTube Data API
API_VERSION_YOUTUBE_ANALYTICS = 'v2'                        # YouTube Analytics API
API_VERSION_YOUTUBE_DATA = 'v3'                             # YouTube Data API
CLIENT_SECRETS_FILE = 'secret.json'
TOKEN_FILE = 'token.pickle'



def load_credentials(scopes):
    creds = None

    # We check whether a token has already been created
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Refresh Token      
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds



def get_service(api_name, api_version, scopes):
    credentials = load_credentials(scopes)
    return build(api_name, api_version, credentials=credentials)

# Function to be called to use YouTube Analytics API
def youtube_analytics_service():
    youtube_analytics = get_service(API_SERVICE_NAME_YOUTUBE_ANALYTICS, API_VERSION_YOUTUBE_ANALYTICS, SCOPES)
    return youtube_analytics

# Function to be called to use YouTube DATA API
def youtube_data_service():
    youtube_data = get_service(API_SERVICE_NAME_YOUTUBE_DATA, API_VERSION_YOUTUBE_DATA, SCOPES)
    return youtube_data