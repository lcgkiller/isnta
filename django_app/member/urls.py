from django.conf.urls import url
from . import views

app_name = 'member'

urlpatterns = [
    # 로그인
    url(r'^login/$', views.login, name='login'),
    url(r'^login/facebook/', views.facebook_login, name='facebook_login'),
    url(r'^logout/$', views.logout, name='logout'),

    # 회원가입
    url(r'^signup/$', views.signup, name='signup'),

    # 프로필
    url(r'^profile/$', views.profile, name='my_profile'),
    url(r'^profile/(?P<user_pk>\d+)/$', views.profile, name='profile'),

    # 팔로우 토글
    url(r'^follow-toggle/(?P<user_pk>\d+)/$', views.follow_toggle, name='follow_toggle'),

    # 프로필 에딧
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit')

]