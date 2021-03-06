from django.conf.urls import url
from .. import views

app_name = 'posts'

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<post_pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^delete/(?P<post_pk>[0-9]+)/$', views.post_delete, name='post_delete'),
    url(r'^modify/(?P<post_pk>[0-9]+)/$', views.post_modify, name='post_modify'),

    # 좋아요
    url(r'^(?P<post_pk>[0-9]+)/like-toggle/$', views.post_like_toggle, name='post_like_toggle'),

    # comment
    url(r'^(?P<post_pk>[0-9]+)/comment/create/$', views.comment_create, name='comment_create'),
    url(r'^comment/(?P<comment_pk>[0-9]+)/modify/$', views.comment_modify, name='comment_modify'),
    url(r'^comment/(?P<comment_pk>[0-9]+)/delete/$', views.comment_delete, name='comment_delete'),

    # 해시태그
    url(r'^tag/(?P<tag_name>\w+)/$', views.hashtag_post_list, name='hashtag_post_list'),

    # 유튜브
    url(r'^youtube/search/$', views.youtube_search, name='youtube_research_default'),
    url(r'^youtube/post/create/$', views.post_create_with_video, name='youtube_post_create')

]

