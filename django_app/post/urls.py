from django.conf.urls import url

from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<post_pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^delete/(?P<post_pk>[0-9]+)/$', views.post_delete, name='post_delete'),
    url(r'^modify/(?P<post_pk>[0-9]+)/$', views.post_modify, name='post_modify'),
    url(r'^comment_add/(?P<post_pk>[0-9]+)/$', views.comment_create, name='comment_add')
]

