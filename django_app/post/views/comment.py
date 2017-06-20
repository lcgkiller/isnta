from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from post.decorators import comment_owner
from ..forms import CommentForm
from ..models import Post, Comment

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

@comment_owner
@login_required
def comment_modify(request, comment_pk):
    # get_object_or_404를 이용해서 Comment 객체 가져오기
    comment = get_object_or_404(Comment, pk=comment_pk)
    next = request.GET.get('next')
    if request.method == 'POST':
        # Form을 이용해 업데이트 (data에 포함된 부분만  update됨)
        form = CommentForm(data=request.POST, instance=comment)
        form.save()
        if next:
            return redirect(next)
        return redirect('posts:post_detail', post_pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
    }
    return render(request, 'post/comment_modify.html', context)


@comment_owner
@require_POST
@login_required
def comment_delete(request, post_pk, comment_pk):
    # comment_delete 이후에 원래 페이지로 돌아갈 수 있도록 처리해보기
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    comment.delete()
    return redirect('posts:post_detail', post_pk=post.pk)

