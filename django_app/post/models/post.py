from django.db import models
from django.conf import settings
from utils.fields import CustomImageField

__all__ = (
    'Post',
    'PostLike',
)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = CustomImageField(upload_to='post', blank=True)
    video = models.ForeignKey('Video', blank=True, null=True) #(0627) 추가
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    my_comment = models.OneToOneField(
        'Comment',
        blank=True,
        null=True,
        related_name='+'
    )  # Post 작성시 내용 (+는 역참조가 없음을 의미)

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_posts',
        through='PostLike'  # makemigrations는 가능하지만, migrate는 안되기 때문에 fake옵션을 주고 수정
    )

    class Meta:
        ordering = ['-pk', ]

    def add_comment(self, user, content):
        # 자신을 post로 갖고, 전달받은 user를 author로 가지며, content를 content 필드내용으로 넣는 Comment 객체를 생성
        return self.comment_set.create(author=user, content=content)

    @property
    def like_count(self):
        return self.like_users.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


