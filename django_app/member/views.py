from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import \
    authenticate, \
    login as django_login, \
    logout as django_logout \

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
