from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from post.decorators import post_owner
from post.forms import CommentForm
from ..forms import PostForm
from ..models import Post, Tag

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage  # (0620) # 페이지네이터

User = get_user_model()  # get_user_model : 자동으로 Django에서 인증에 사용되는 User모델클래스를 리턴

__all__ = (
    'post_modify',
    'post_create',
    'post_delete',
    'post_detail',
    'post_list',
    'hashtag_post_list',
)


def post_list_original(request):
    # 1. 모든 Post 목록을 'post'라는 key로 context에 담아 return render 처리
    # 2. post/post_list.html을 템플릿으로 사용

    # (0620) 숙제
    # 1. post_list와 hashtag_post_list에서 pagination을 이용해서
    #       한 번에 10개씩만 표시하도록 수정
    #       https://docs.djangoproject.com/en/1.11/topics/pagination/
    # 2. 좋아요 버튼 구현 및 좋아요 한 사람 목록 출력

    posts = Post.objects.all()

    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }

    return render(request, 'post/post_list.html', context)


def post_list(request):
    # (0621) 위 post_list_original() 함수뷰에서 posts가 Paginator를 통해 5개씩 출력하도록 수정

    # 전체 Post 목록 QuerySet생성 (아직 평가되지 않은 상태)
    all_posts = Post.objects.all()

    # GET 파라미터에서 'page'값을 page_num 변수에 할당 (1. 오브젝트, 2. 개당 출력 갯수)
    paginator = Paginator(all_posts, 2)
    page = request.GET.get('page', 1)

    try:
        # Page형 오브제트를 돌려준다.
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    index = posts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        'posts': posts,
        'page_range': page_range,
        'comment_form': CommentForm(),
    }

    return render(request, 'post/post_list.html', context)


def post_like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post_id = post.pk
    liked = False
    if request.session.get('has_liked_'+str(post_id), liked):
        liked = True
        print("linked {}_{}".format(liked, post_id))
    context = {
        'post': post,
        'liked': liked
    }
    return render(request, 'post/post_list.html', context)


def like_count_post(request):
    liked = False
    if request.method == 'GET':
        post_id = request.GET['post_id']
        post = Post.objects.get(id=int(post_id))
        if request.session.get('has_liked_'+post_id, liked):
            print("unlike")
            if post.likes > 0:
                likes = post.likes - 1
                try:
                    del request.session['has_liked_'+post_id]
                except KeyError:
                    print("keyerror")

        else:
            print("like")
            request.session['has_liked_'+post_id] = True
            likes = post.likes + 1

    post.likes = likes
    post.save()
    return HttpResponse(likes, liked)


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
    if request.method == 'POST':
        post.delete()
        return redirect('posts:post_list')
    else:
        context = {
            'post': post,
        }
        return render(request, 'post/post_delete.html', context)
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


def hashtag_post_list(request, tag_name):
    # 1. template 생성
    #   post/hashtag_post_list.html
    #   tag_name과 post_list, post_count변수를 전달받아 출력
    #   tag_name과 post_count는 최상단 제목에 사용
    #   post_list를 순회하며 post_thubmnail에 해당하는 html을 구성해서 보여줌

    # 2. 쿼리셋 작성
    #   특정 tag_name이 해당 Post에 포함된 Comment의 tags에 포함되어있는 Post목록 쿼리 생성
    #       posts = Post.objects.filter()

    # 3. urls.py와 이 view를 연결
    # 4. 해당 쿼리셋을 적절히 리턴
    # 5. Comment의 make_html_and_add_tags()메서드의 a태그를 생성하는 부분에 이 view에 연결되는 URL을 삽입


    # 6. 이후 해당 목록을 적절히 리턴해주고 보여주는 html render

    tag = get_object_or_404(Tag, name=tag_name)

    # Post에 달린 댓글의 Tag까지 검색할 때
    # posts.objects.filter(comment_set__tags=tag).distinct()

    # Post의 my_comment에 있는 Tag만 검색할 때
    posts = Post.objects.filter(my_comment__tags=tag)
    posts_count = posts.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 3)

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    index = pages.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'tag': tag,
        'posts': posts,
        'posts_count': posts_count,
        'pages': pages,
        'page_range': page_range
    }
    return render(request, 'post/hashtag_post_list.html', context)