#
import requests
from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

__all__ = (
    'search',
)

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

    DEVELOPTER_KEY = settings.YOUTUBE_SECRET_CODE,
    YOUTUBE_API_SERIVCE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERIVCE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPTER_KEY)
    search_response = youtube.search().list(
        part='snippet',
        maxResults='10',
        type='video',
        q=q,
    ).execute()

    videos = []
    channels = []
    playlists = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))

        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))

    print("Videos:\n", "\n".join(videos), "\n")
    print("Channels:\n", "\n".join(channels), "\n")
    print("Playlists:\n", "\n".join(playlists), "\n")


if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()

try:
    search(args)
except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
