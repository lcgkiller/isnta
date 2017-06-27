import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from config import settings
from post.models import Video, Post, Comment
from utils import youtube

__all__ = (
    'youtube_search',
    'post_create_with_video',
)

def youtube_search_orginal(request):
    # [1] 기초숙제 : 검색결과를 DB에 저장하고, 해당내용을 템플릿에서 보여주기 (0626)
    # 1. 유튜브 영상을 저장할 class Video(models.Model) 생성
    # 2. 검색결과의 videoId를 Video의 youtube_id필드에 저장
    # 3. 검색결과에서 videoId가 Video의 youtube_id와 일치하는 것이 없을 경우 새 Video객체를 만들어 DB에 저장
    # 4. 이후 검색결과가 아닌 자체 DB에서 QuerySet을 만들어 필터링
    # 5. 빈칸으로 구분되면 and 검색

    # [2] 심화숙제 : 위 과제로 완성된 검색결과에서 '포스팅하기' 버튼을 구현, Post가 YouTube영상을 포함하도록 함
    # 1. 검색결과에서 '포스팅하기'버튼을 누르면 해당 Video와 연결된 Post 생성
    # 2. post_list에서 재생화면 구현
    # 3. mycomment를 타이틀로 등록

    # search list API를 이용해서 request.GET.get('q')에 데이터가 있을 경우 검색결과를 requests.get을 사용한 결과를 변수에 할당하고 해당 변수를 템플릿에서 표시

    url = "https://www.googleapis.com/youtube/v3/search"
    q = request.GET.get('q')
    context = {}
    if q:
        url_params = {
            'part': 'snippet',
            'key': settings.YOUTUBE_SECRET_CODE,
            'maxResults': '10',
            'type': 'video',
            'q': q
        }
        response = requests.get(url, params=url_params)
        result = response.json()

        for item in result['items']:
            # CustomMnager를 사용해 object 생성
            Video.objects.create_from_search_result(item)

        # 제목내에 검색어가 포함되는지 여부
        # videos = Video.objects.filter(title__contains=q)
        # 제목과 설명에 포함되는지
        # videos = Video.objects.filter(Q(title__contains=q) | Q(description__contains=q))
        # 검색어가 빈칸단위로 구분되어있을 때, 빈칸으로 split한 값들을 각각 포함하고 있는지 and 연산
        # videos = Video.objects.all()

        # 원시적인 방법 ( & 연산 )
        # for cur_q in q.split(' '):
        #     videos.filter(title__contains=cur_q)

        # regex ( and 연산 )
        # re_pattern = ''.join(['(?=.*{})'.format(item) for item in q.split()])
        # videos = Video.objects.filter(title__regex=r'')

        # regex ( or 연산 )
        re_pattern = '|'.join(['({})'.format(item) for item in q.split()])

        videos = Video.objects.filter(
            Q(title__regex=r'{}'.format(re_pattern)) |
            Q(description__regex=r'{}'.format(re_pattern))
        )
        context = {
            'videos': videos,
            're_pattern': re_pattern,
        }

    return render(request, 'post/youtube_search.html', context)

def youtube_search(request, Q=None):
    context = dict()
    q = request.GET.get('q')
    if q:
        # YouTube 검색부분을 패키지화
        data = youtube.search(q)
        print("데이터 출력 :",data)
        for item in data['items']:
            Video.objects.create_from_search_reslt(item)
        re_pattern = ''.join(['(?=.*{})'.format(item) for item in q.split()])
        videos = Video.objects.filter(
            Q(title__regex=re_pattern) |
            Q(description__regex=re_pattern)
        )

        context['videos'] = videos
    return render(request, 'post/youtube_search.html', context)
@require_POST
@login_required
def post_create_with_video(request):
    # POST 요청에서 video_pk값을 받음
    video_pk = request.POST['video_pk']

    # 받은 video_pk에 해당하는 Video 인스턴스
    video = get_object_or_404(Video, pk=video_pk)

    # 해당 video를 갖는 Post 생성
    post = Post.objects.create(
        author=request.user,
        video=video,
    )

    # 생성한 Post객체의 my_comment에 해당하는 Comment 생성
    post.my_comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=video.title
    )

    return redirect('posts:post_detail', post_pk=post.pk)