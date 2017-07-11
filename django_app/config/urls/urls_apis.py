from django.conf.urls import include, url

urlpatterns = [
    url(r'^post/', include('post.urls.urls_apis'))
]