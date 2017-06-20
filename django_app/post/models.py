"""
member application 생성
    User 모델 구현
        username, nickname
이후 해당 User 모델을 Post나 Comment에서 author, User항목으로 참조
"""
from django.conf import settings
from django.db import models
import re
from django.contrib.auth.models import User


# Create your models here.
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post', blank=True)
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


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(null=True, blank=True)
    html_content = models.TextField(blank=True)  # 0620 추가(해쉬태그)
    tags = models.ManyToManyField('Tag')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommentLike',
        related_name="like_comments"
    )

    # 0620 해쉬태그 기능
    def save(self, *args, **kwargs):  # save 메서드는 아무것도 돌려주지 않는다.
        super().save(*args, **kwargs)
        self.make_html_content_and_add_tags()

    def make_html_content_and_add_tags(self):
        # ex) 주말경기 #축구 #야구 인스타
        #   --> '주말경기 <a href='#'>축구</a><a href='#'>야구</a> 인스타
        # 해당내용을 self.html_content에 대입

        # 해시태그에 해당하는 정규표현식
        p = re.compile(r'(#\w+)')

        # 정규표현식의 findall 메서드로 해시태그가 걸린 문자열을 가져옴
        tag_name_list = re.findall(p, self.content)
        ori_content = self.content

        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name.replace('#', ''))
            change_tag = '<a href="{url}" class="hash-tag">{tag_name}</a>'.format(
                # url=reverse('posts:hashtag_post_list', args=[tag_name.replace('#', '')]),
                url=reverse('posts:hashtag_post_list', kwargs={'tag_name': tag_name.replace('#', '')}),
                tag_name=tag_name
            )
            ori_content = re.sub(r'{}(?![<\w])'.format(tag_name), change_tag, ori_content, count=1)

            if not self.tags.filter(pk=tag.pk).exists():
                self.tags.add(tag)

        self.html_content = ori_content
        super().save(update_fields=['html_content'])


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag({})'.format(self.name)
