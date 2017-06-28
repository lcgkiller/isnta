import requests
from django.conf import settings
from googleapiclient.discovery import build


def search_original(q):
    url = "https://www.googleapis.com/youtube/v3/search"
    url_params = {
        'part': 'snippet',
        'key': settings.YOUTUBE_SECRET_CODE,
        'maxResults': '10',
        'type': 'video',
        'q': q
    }
    response = requests.get(url, params=url_params)
    data = response.json()
    return data


def search(q):
    # google youtube api client를 이용

    DEVELOPER_KEY = settings.YOUTUBE_SECRET_CODE
    YOUTUBE_API_SERIVCE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERIVCE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=q,
        part='id,snippet',
        maxResults=10,
        type='video',
    ).execute()

    return search_response
