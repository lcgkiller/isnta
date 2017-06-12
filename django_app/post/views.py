from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import Post


def index(request):
    return HttpResponse("Hello World")


def post_list(request):
    # 1. 모든 Post 목록을 'post'라는 key로 context에 담다 return render 처리
    # 2. post/post_list.html을 템플릿으로 사용
    # 3.
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }

    return render(request, 'post/post_list.html', context)
