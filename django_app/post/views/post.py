from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from post.decorators import post_owner
from post.forms import CommentForm
from ..forms import PostForm
from ..models import Post

User = get_user_model()  # get_user_model : 자동으로 Django에서 인증에 사용되는 User모델클래스를 리턴

__all__ = (
    'post_modify',
    'post_create',
    'post_delete',
    'post_detail',
    'post_list'
)


def post_list(request):
    # 1. 모든 Post 목록을 'post'라는 key로 context에 담아 return render 처리
    # 2. post/post_list.html을 템플릿으로 사용

    # (0620) 각 포스트에 대해 최대 4개의 댓글을 보여주도록 템플릿에 설정
    # 각 post 하나당 CommentForm을 하나씩 가지도록 리스트 컴프리헨션 사용
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }

    return render(request, 'post/post_list.html', context)


# 숙제
def post_detail(request, post_pk):
    # post_pk에 해당하는 Post객체를 리턴
    print("디테일 페이지 POST_PK : ", post_pk)

    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist as e:
        # 선택지 1. 404 Not Found 띄워주기
        # return HttpResponseNotFound('Post Not Found, detail : {}'.format(e))

        # 선택지 2. 다시 post_list 페이지로 돌아가기 ( 어디로 돌아갈 지 url 기입)
        # 2-1 redirect 사용
        # return redirect('posts:post_list')
        # 2-2 HttpResponseRedirect를 사용
        # return HttpResponseRedirect('post_list')
        url = reverse('posts:post_list')  # 뷰 이름을 그대로 적어준다.
        return HttpResponseRedirect(url)

    context = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', context)


@login_required
def post_create(request):
    # POST요청을 받아 Post 객체를 생성 후 post_list 페이지로 redirect

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('member:login')

        # user = User.objects.first()
        #     post = Post.objects.create(
        #         author = user,
        #         photo=request.FILES['file'],
        #     )
        #
        #     comment_string = request.POST.get('comment', '')
        #     if comment_string:
        #         # 댓글로 사용할 문자열이 전달된 경우 위에서 생성한 post객체에 연결되는 Comment 객체를 생성
        #         post.comment_set.create(
        #             # 임의 유저를 사용하고, 실제 로그인된 사용자로 바꿔주어야 함.
        #             author=user,
        #             content=comment_string,
        #         )

        ###### 철규
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # ModelForm의 save()메서드를 사용해 Post객체를 가져온다.
            post = form.save(author=request.user)
            return redirect('posts:post_detail', post_pk=post.pk)

    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


@post_owner
@login_required
def post_modify(request, post_pk):
    # 수정하고자 하는 Post 객체를 얻어온다.
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_pk)

    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'post/post_modify.html', context=context)


@post_owner
@login_required
def post_delete(request, post_pk):
    # post_pk에 해당하는 Post에 대한 delete 요청만을 받음
    # 처리 만료후에는 post_list페이지로 redirect
    post = get_object_or_404(Post, pk=post_pk)
    post.delete()
    return redirect('posts:post_list')
    # if request.method == "POST":
    #     yes_or_no = request.POST.get('delete_yes_or_no')
    #     print("말해 :", yes_or_no)
    #
    #     if yes_or_no == "yes":
    #         post.delete()
    #         return redirect('posts:post_list')
    #
    #     elif yes_or_no == "no":
    #         return redirect('posts:post_list')
    # return render(request, 'post/post_delete.html')
