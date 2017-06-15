from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import \
    authenticate, \
    login as django_login, \
    logout as django_logout \
 \
 \
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
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # user 객체가 있는 경우, Django 세션을 이용해 request와 user객체를 이용해 로그인 처리를 진행한다.
            # 이후의 request/response에서는 사용자가 인증된 상태로 통신이 이루어진다.
            django_login(request, user)
            return redirect('posts:post_list')
        else:
            return HttpResponse("Login invalid!")

    else:
        # 02. 이미 로그인 된 상태일 경우에는 post_list로 redirect
        if request.user.is_authenticated:
            return redirect("posts:post_list")
        return render(request, 'member/login.html')


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
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username).exists():
            return HttpResponse('Username is already exists')
        elif password1 != password2:
            return HttpResponse('패스워드가 다릅니다.'.format(username))

        user = User.objects.create_user(username=username, password=password1)
        django_login(request, user)
        return redirect("posts:post_list")

    else:
        return render(request, 'member/signup.html')