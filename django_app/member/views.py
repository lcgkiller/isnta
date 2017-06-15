from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

# Create your views here.
def login(request):
    # member/login.html 생성
    #   username, password, button이 있는 html 생성
    #   POST이 올경우 좌측 코드를 기반으로 로그인 완료 후 post_list로 이동
    #   실패할 경우 HttpResponse로 'Login invalid!' 띄워주기

    # member/urls.py 생성
    #   /member/login/으로 접근시 이 view로 오도록 설정
    #   config/urls.py에 member/urls.py를 include
    #       member/urls.py에 app_name설정으로 namespace 설정

    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(request, username=username, password=password)
    if request.method == "POST":
        if user is not None:
            login(request, user)
            return redirect('posts:post_list')
        else:
            return HttpResponse("Login invalid!")

    else:
        return render(request, 'member/login.html')