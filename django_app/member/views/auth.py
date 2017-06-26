import code
from pprint import pprint

import requests
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect, render

from config import settings
from member.forms import LoginForm, SignupForm

from django.contrib.auth import \
    login as django_login, \
    logout as django_logout

__all__ = (
    'login',
    'logout',
    'signup',
    'facebook_login',
)


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


def facebook_login(request):
    # Facebook_login view가 처음 호출될 때  유저가 Facebook login dialog에서 로그인 후, 페이스북에서 우리 서비스(Consumer)쪽으로 GET 파라미터를 이용해 'code'를 전달해준다. 전달받는 코드는 위 uri_direct
    # facebook_login view가 처음 호출될 때 'code' request GET parameter받음
    # code라는 부분이 없으면 로그인이 안된 것임. 족, 코드가 있을 때만 진행
    code = request.GET.get('code')
    app_access_token = '{}|{}'.format(
        settings.FACEBOOK_APP_ID,
        settings.FACEBOOK_SECRET_CODE,
    )

    def add_message_and_redirect_referer():
        """
        # 페이스북 로그인 오류 메시지를 request에 추가하고, 이전 페이지로 redirect
        """
        # 유저용 메세지
        error_message_for_user = 'Facebook login error'
        # request에 에러메세지를 전달
        messages.error(request, error_message_for_user)
        # 이전페이지로 redirect
        return redirect(request.META['HTTP_REFERER'])

    def get_access_token(code):
        """
        code를 받아 액세스토큰 교환 URL에 요청, 이후 해당 액세스 토큰을 반환
        오류 발생시 오류메시지를 리턴
        """
        # 액세스토큰의 코드를 교환할 URL
        url_access_token = 'https://graph.facebook.com/v2.9/oauth/access_token'

        # 이전에 요청했던 redirect_uri와 같은 값을 만들어 줌 (access_token을 요청할 때 필요함)
        redirect_uri = '{}://{}{}'.format(
            request.scheme,
            request.META['HTTP_HOST'],
            request.path,
        )
        # 액세스토큰의 코드 교환
        # uri생성을 위한 params
        url_access_token_params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_SECRET_CODE,
            'code': code,
        }
        # 해당 URL에 get요청 후 결과 (json형식)를 파이썬 object로 변환 (result변수)
        response = requests.get(url_access_token, params=url_access_token_params)
        result = response.json()

        if 'access_token' in result:
            return result['access_token']

        # 액세스토큰 코드교환 결과에 오류가 있을 경우
        # 해당 오류를 request에 message로 넘기고 이전페이지 (HTTP_REFERRER)로 redirect
        elif 'error' in result:
            raise Exception(result['error'])
            # 상세 오류 메세지 (개발자용)
            # error_message = 'Facebook login error\n  type: {}\n  message: {}'.format(
            #     result['error']['type'],
            #     result['error']['message']
            # )

        else:
            raise Exception('Unknown error')

    # code키값이 존재하지 않으면 로그인을 더이상 진행하지 않음
    if not code:
        return add_message_and_redirect_referer()
    try:
        access_token = get_access_token(code)
    except Exception as e:
        print(e)
        return add_message_and_redirect_referer()

        # 액세스토큰 검사
