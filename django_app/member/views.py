from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import \
    authenticate, \
    login as django_login, \
    logout as django_logout \

from post.models import Post
from .forms import LoginForm
from .forms import SignupForm

# Create your views here.

from .models import User


def login(request):
    # member/login.html 생성
    #   username, password, button이 있는 html 생성
    #   POST이 올경우 좌측 코드를 기반으로 로그인 완료 후 post_list로 이동
    #   실패할 경우 HttpResponse로 'Login invalid!' 띄워주기

    # member/urls.py 생성
    #   /member/login/으로 접근시 이 view로 오도록 설정
    #   config/urls.py에 member/urls.py를 include
    #       member/urls.py에 app_name설정으로 namespace 설정

    if request.method == "POST":

        # if user is not None:
        #     # user 객체가 있는 경우, Django 세션을 이용해 request와 user객체를 이용해 로그인 처리를 진행한다.
        #     # 이후의 request/response에서는 사용자가 인증된 상태로 통신이 이루어진다.
        #     django_login(request, user)
        #     return redirect('posts:post_list')


        ### Form 클래스 사용
        # Bound Form 생성
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # is_valid를 실행하면 clean 메서드가 실행된다.
            user = form.cleaned_data['user']
            django_login(request, user)

            # 일반적인 경우 post_list로 이동하지만, GET parameter의 next 속성값이 있을 경우 해당 URL로 이동
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('posts:post_list')


    # GET 요청
    else:
        # 02. 이미 로그인 된 상태일 경우에는 post_list로 redirect
        if request.user.is_authenticated:
            return redirect("posts:post_list")

        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('posts:post_list')


def signup(request):
    # member/signup.html을 사용
    #   1. username, password1, passwords2를 받아 회원가입.
    #   2. 기존에 존재하는 유저인지 검사
    #   3. password1, 2가 일치하는지 검사
    #   4. 각각의 경우를 검사해서 틀릴 경우 오류메시지 리턴
    #   5. 가입성공시 로그인시키고 post_list로 redirect

    if request.method == "POST":

        ### Form을 사용하지 않는 경우
        # form = SignupForm(data=request.POST)
        # username = request.POST['username']
        # password1 = request.POST['password1']
        # password2 = request.POST['password2']
        # if User.objects.filter(username=username).exists():
        #     return HttpResponse('Username is already exists')
        # elif password1 != password2:
        #     return HttpResponse('패스워드가 다릅니다.'.format(username))
        #
        # user = User.objects.create_user(username=username, password=password1)


        ### Form을 사용한 경우
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.create_user()
            print("유저 누구? ", user)
            # 위에서 생성한 유저를 로그인 시킨 후, post_list뷰로 이동
            django_login(request, user)
            return redirect("posts:post_list")

    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'member/signup.html', context)


def profile(request, user_pk=None):
    NUM_POST_PER_PAGE = 3
    # 0. urls.py에 연결
    # 1. User_pk에 해당하는 User를 cur_user키로 render
        # 또는 user = get_object_or_404(User, pk=user_pk)

    # 2. member/profile.html작성, 해당 user정보 보여주기
    # 2-1 해당 user의 follwers, following 목록 보여주기


    # 3 현재 로그인한 유저가 해당 유저(cur_user)를 팔로우하고 있는지 여부 보여주기
        # 3-1 팔로우하고 있다면 '팔로우 해제'버튼, 아니라면 '팔로우'버튼 띄워주기

    # 4. -> def follow_toggle(request) 뷰 생성


    """
    1. GET parameter로 'page'를 받아 처리
    2. page가 1일 경우 Post의 author가 해당 User인 Post 목록을 
        -created_date 순서로 page * 9 만큼의 QuerySet을 생성해서 리턴
        
        만약, 실제 Post 개수보다 큰 page가 왔을 경우, 최대한의 값을 보여준다.
        int로 변환 불가능한 경우, except처리
        1보다 작은값일 경우 except 처리 
        오지 않을 경우 page=1로 처리
    """

    # 1. GET 파라미터 처리
    page = request.GET.get('page', 1)
    try:
        page = int(page) if int(page) > 1 else 1
    except ValueError:
        page = 1
    except Exception as e:
        page = 1
        print(e)


    """
        3. def follow_toggle(request, user_pk)
          위 함수기반 뷰를 구현
                login_required
                required POST
            데코레이터를 사용(필요하다면 추가)
            처리 후 next값을 받아 처리하고, 없을 경우 해당 User의 Profile로 이동

        ** extra. 유저 차단기능 만들어보기
            Block여부는 Relation에서 다룸
                1. followers, following에 유저가 나타나면 안됨
                2. block_users로 차단한 유저 목록 QuerySet 리턴
                3. follow, unfollow 기능을 하기전에 block된 유저인지 확인
                4. block처리시 follow상태는 해제되어야 함 (동시적용 불가)
                5. 로그인 시 post_list에서 block_users의 글은 보이지 않도록 함. 

    """
    if user_pk:
        user = get_object_or_404(User, pk=user_pk)

    else:
        user = request.user

    # page * 9만큼의 Post QuerySet을 리턴

    posts = user.post_set.order_by('-created_date')[:page * NUM_POST_PER_PAGE]
    post_count = user.post_set.count()
    # next_page = 현재 page에서 보여주는 Post개수보다 post_count가 클 경우 전달받은 page + 1, 아닐 경우 None 할당
    next_page = page + 1 if post_count > page * NUM_POST_PER_PAGE else None
    context = {
        'cur_user' : user,
        'posts': posts,
        'post_count': post_count,
        'page': page,
        'next_page': next_page,
    }

    return render(request, 'member/profile.html', context)


    # if request.method == "POST":
    #     print("포스트 :", request.POST)
    #
    # else:
    #     posts = user.post_set.all().order_by('-created_date')
    #     posts_count = posts.count()
    #
    #     paginator = Paginator(posts, 3)
    #
    #     try:
    #         pages = paginator.page(int(page))
    #     except PageNotAnInteger:
    #         pages = paginator(1)
    #     except EmptyPage:
    #         pages = paginator.page(paginator.num_pages)
    #     except CustomException as e:
    #         print("1보다 작은 값 ", e)
    #
    #     index = pages.number - 1
    #     max_index = len(paginator.page_range)
    #     start_index = index - 3 if index >= 3 else 0
    #     end_index = index + 3 if index <= max_index - 3 else max_index
    #     page_range = paginator.page_range[start_index:end_index]

        # context = {
        #     'posts': posts,
        #     'posts_count': posts_count,
        #     'pages': pages,
        #     'page_range': page_range,
        # }


@login_required
def follow_toggle(request, user_pk):
    pass


class CustomException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value














