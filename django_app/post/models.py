"""
member application 생성
    User 모델 구현
        username, nickname
이후 해당 User 모델을 Post나 Comment에서 author, User항목으로 참조
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_posts',
        through='PostLike'  # makemigrations는 가능하지만, migrate는 안되기 때문에 fake옵션을 주고 수정
    )

    tags = models.ManyToManyField('Tag')

    def add_comment(self, user, content):
        # 자신을 post로 갖고, 전달받은 user를 author로 가지며, content를 content 필드내용으로 넣는 Comment 객체를 생성
        return self.comment_set.create(author=user, content=content)

    def add_tag(self, tag_name):
        # tags에 tag매개변수로 전달된 값(str) name으로 갖는 Tag객체를 (이미 존재하면) 가져오고 없으면 생성하여 자신의 tags에 추가

        tag, tag_created = Tag.objects.get_or_create(name=tag_name)

        if not self.tags.filter(name=tag.id).exists():
            self.tag.add(tag)

    @property
    def like_count(self):
        return self.like_users.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommentLike',
        related_name="like_comments"
    )


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    # tag = models.TextField()
    tag = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag({})'.format(self.tag)
