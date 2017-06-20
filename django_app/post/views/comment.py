from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from ..forms import CommentForm
from ..models import Post


__all__ = (
    'comment_modify',
    'comment_create',
    'comment_delete',
)

@require_POST
@login_required
def comment_create(request, post_pk):
    # URL에 전달되어온 post_pk로 특정 Post객체를 가져온다.
    post = get_object_or_404(Post, pk=post_pk)

    # URL의 get parameter의 'next'값을 가져온다.
    next = request.GET.get('next')

    # CommentForm data binding
    form = CommentForm(request.POST)

    # form이 유효한 경우 Comment 생성
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    # form이 유효하지 않을 경우, 현재 request에 error메시지 추가
    else:
        result = '<br>'.join(['<br>'.join(v) for v in form.errors.values()])
        messages.error(request, result) # (0620) 에러메시지

    if next:
        return redirect(next)
    return redirect('posts:post_detail', post_pk=post_pk)


        # if request.method == "POST":
        #     content = request.POST.get('content', '')
        #     user = User.objects.first()
        #     post = Post.objects.get(pk=post_pk)
        #     post.add_comment(user, content)



def comment_delete(request, post_pk, comment_pk):
    # POST요청을 받아 Comment 객체를 delete, 이후 post_detail 페이지로 redirect
    # CommentForm을 만들어서 해당 Form안에서 생성/수정가능하도록 사용
    post = Post.objects.get(pk=post_pk)
    comment = post.comment_set.get(pk=comment_pk)

    if request.method == "POST":
        yes_or_no = request.POST.get('delete_yes_or_no')
        if yes_or_no == "yes":
            comment.delete()
            return redirect('posts:post_detail', post_pk)

    elif request.method == "GET":
        context = {
            'comment': comment
        }
        return render(request, 'comment/comment_delete.html', context)

def comment_modify(request):
    pass