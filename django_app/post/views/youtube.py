import requests
from django.shortcuts import render, redirect

from config import settings

__all__ = (
    'youtube_search',
)
def youtube_search(request):
    # [1] 기초숙제 : 검색결과를 DB에 저장하고, 해당내용을 템플릿에서 보여주기 (0626)
        # 1. 유튜브 영상을 저장할 class Video(models.Model) 생성
        # 2. 검색결과의 videoId를 Video의 youtube_id필드에 저장
        # 3. 검색결과에서 videoId가 Video의 youtube_id와 일치하는 것이 없을 경우 새 Video객체를 만들어 DB에 저장
        # 4. 이후 검색결과가 아닌 자체 DB에서 QuerySet을 만들어 필터링

    # [2] 심화숙제 : 위 과제로 완성된 검색결과에서 '포스팅하기' 버튼을 구현, Post가 YouTube영상을 포함하도록 함
        # 1. 검색결과에서 '포스팅하기'버튼을 누르면 해당 VIdeo와 연결된 Post 생성
        # 2. post_list에서 재생화면 구현

    # search list API를 이용해서 request.GET.get('q')에 데이터가 있을 경우 검색결과를 requests.get을 사용한 결과를 변수에 할당하고 해당 변수를 템플릿에서 표시
    url = "https://www.googleapis.com/youtube/v3/search"
    q = request.GET.get('q')
    if q:
        url_params = {
            'part': 'snippet',
            'key': settings.YOUTUBE_SECRET_CODE,
            'maxResults': '10',
            'type': 'video',
            'q': q
        }
        response = requests.get(url, params=url_params)
        # 각 for문을 순회하면서 items를 Video로 저장. (Video.objects.filter(title__contains=q) 있으면 넘어가고 없으면
        context = {
            'response': response.json(),
        }
    else:
        context = {}

    return render(request, 'post/youtube_search.html', context)
