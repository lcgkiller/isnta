from unittest import TestCase
from django.urls import reverse, resolve
from ... import views


# auth.py 내 login 뷰 테스트


class LoginViewTest(TestCase):

    VIEW_URL = '/member/login/'
    VIEW_URL_NAME = 'member:login'

    def test_url_equal_reverse_url_name(self):
        # 주어진 VIEW_URL과 VIEW_URL_NAME을 reverse()한 결과가 같은지 검사
        self.assetEqual(self.VIEW_URL, reverse(self.VIEW_URL_NAME))

    # 해당 url을 사용하고 있는지 여부를 resolve 함수를 이용해 특정 URL이 참조하는 view를 검색
    def test_url_resolves_to_login_view(self):
        found = resolve(self.VIEW_URL)
        print("파운드 :", found)
        print(found.func)
        print(views.login)
        # 특정 view에 해당하는 함수 (.func속성)과 views.login함수가 같은지 확인
        self.assertEqual(found.func, views.login())

    def test_user_login_template(self):
        url = reverse(self.VIEW_URL_NAME)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'member/login.html')
