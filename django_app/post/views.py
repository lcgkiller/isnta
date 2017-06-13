from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .forms import ContactForm  # 버튼
from .models import Post

# Create your views here.
from .models import Post


def index(request):
    return HttpResponse("Hello World")


def post_list(request):
    # 1. 모든 Post 목록을 'post'라는 key로 context에 담아 return render 처리
    # 2. post/post_list.html을 템플릿으로 사용
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }

    return render(request, 'post/post_list.html', context)


# 숙제
def post_detail(request, post_pk):
    # post_pk에 해당하는 Post객체를 리턴
    print("POST_PK : ", post_pk)

    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist as e:
        # 선택지 1. 404 Not Found 띄워주기
        # return HttpResponseNotFound('Post Not Found, detail : {}'.format(e))

        # 선택지 2. 다시 post_list 페이지로 돌아가기 ( 어디로 돌아갈 지 url 기입)
            # 2-1 redirect를 사용
        return redirect('posts:post_list')
            # 2-2 HttpResponseRedirect
        # return HttpResponseRedirect('post_list')

    context = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', context)


def post_create(request):
    # POST요청을 받아 Post 객체를 생성 후 post_list 페이지로 redirect
    if request.method == "GET":
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(request, 'post/post_create.html', context)
    elif request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        print("벨리드 ", form.is_valid())
        if form.is_valid():
            print("클린데이터 : ", form.is_valid())
            image = Post(photo=request.FILES['image'])
            user = form.cleaned_data['user']
            post = Post.objects.create(author=user, photo=image)
            form.save()
            return redirect('post_list', pk=post.pk)

        else:
            context = {
                'form': form
            }
            return render(request, 'post/post_create.html', context)


def post_delete(request, post_pk):
    # post_pk에 해당하는 Post에 대한 delete 요청만을 받음
    # 처리 만료후에는 post_list페이지로 redirect
    pass


def post_modify(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        data = request.POST
        author = data['author']
        text = data['text']


def comment_create(request, post_pk):
    # POST 요청을 받아 Comment 객체를 생성 후 post_detail 페이지로 redirect
    pass


def comment_delete(request, post_pk, comment_pk):
    # POST요청을 받아 Comment 객체를 delete, 이후 post_detail 페이지로 redirect
    pass
