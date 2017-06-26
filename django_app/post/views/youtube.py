from django.shortcuts import render

__all__ = (
    'youtube_search',
)
def search(request, q=None):
    return render(request, 'post/youtube_search.html.html')
