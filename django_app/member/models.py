import re

import requests
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models

from utils.fields import CustomImageField


class UserManager(DefaultUserManager):

    def get_or_create_facebook_user(self, user_info):
        # USER_INFO의 id값이 혹여나 중복되는 걸 막음
        username = '{}_{}_{}'.format(
            self.model.USER_TYPE_FACEBOOK,
            settings.FACEBOOK_APP_ID,
            user_info['id']
        )

        user, user_created = self.get_or_create(
            username=username,
            user_type=self.model.USER_TYPE_FACEBOOK,
            defaults={  # 페이스북 id는 고유하지만, 다른 프로필은 바꿀 수 있기 때문에 디폴트 값을 지정
                'last_name': user_info.get('last_name', ''),
                'first_name': user_info.get('first_name', ''),
                'email': user_info.get('email', ''),
            }
        )

        # 새로운 유저가 생성될 때만 프로필 이미지를 받아옴
        if user_created:
            # 프로필 이미지 다운로드 (메모리에 파일 객체를 임시로 만듦으로써)
            """
            https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/15965492_301767310224882_6951290062601071961_n.jpg?oh=94c5a85d8205ae4b7cfe7d2a307b4d23&oe=59D4453A'
            """
            url_picture = user_info['picture']['data']['url']  # URL

            p = re.compile(r'.*\.([^?]+)')  # 파일 확장자를 가져와 유저 고유의 파일명을 만들어준다.
            file_ext = re.search(p, url_picture).group(1)
            file_name = '{}.{}'.format(
                user.pk,
                file_ext,
            )

            temp_file = NamedTemporaryFile(delete=False)  # 이미지 파일을 임시저장할 파일객체
            response = requests.get(p, url_picture)  # 프로필 이미지 URL에 대한 get 요청을 함(이미지 다운로드)
            temp_file.write(response.content)  # 요청 결과를 temp_file에 기록

            # ImageField의 save() 메서드를 호출해서 해당 임시파일 객체를 주어진 이름의 파일로 저장한다.
            # 저장하는 파일명은 위에서 만든 <유저pk.주어진파일확장자>
            user.img_profile.save(file_name, File(temp_file))
        return user


class User(AbstractUser):
    """
    동작
        follow : '자신'이 다른사람을 follow 함
        unfollow : 내가 다른 사람들에게 한 follow를 취소함 
    
    속성
        followers : 나를 follow 하는 사람들
        follower : 나를 follow 하고 있는 사람
        following : 내가 follow 하고 있는 사람들
        friends : 나와 서로 follow하고 있는 관계
        friends : 나와 서로 follow하고 있는 모든 관계
        
    
    없음 : 내가 follow하고 있는 사람 1명
    """
    # (0626) 유저모델을 AUTH_USER_MODEL로 사용하도록 settings.py에 설정
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=USER_TYPE_DJANGO)
    nickname = models.CharField(max_length=24, null=True, unique=True)

    # (0623) 커스텀 이미지 필드로 바꿈
    profile_image = CustomImageField(
        upload_to='user',
        blank=True,
        # default_static_image='', # 디폴트값일때 넣어주는 이미지, 실제로는 FileField에는 이 키워드인자가 없다.
                                 # 따라서, utils/custom_imagefiled.py에서 CustomImageField를 오버라이드해준다.
    )

    # (0622)
    relations = models.ManyToManyField(
        'self',                 # 유저테이블끼리의 인스턴스간 관계를 가리키기 위해 'self'를 사용
        through='Relation',     # member_relation 테이블이 새로 생긴다.
        symmetrical=False,
    )

    # (0626)
    # 위에서 만든 CustomUserManager를 objects속성으로 사용
    # User.objects.create_facebook_user() 메서드 실행 가능
    objects = UserManager()

    def __str__(self):
        return self.nickname or self.username


    def follow(self, user):
        # 매개변수로 전달된 user의 형(타입, = 클래스) 검사
        if not isinstance(user, User):
            raise ValueError('"user" argument must <User> class')


        # 해당 user를 follow하는 Relation을 생성한다.
        # 이미 follow 상태일 경우에는 아무일도 하지 않는다.

        # Relatio 모델의 Manager를 사용하는 방법
        Relation.objects.get_or_create(from_user=self, to_user=user)

        # self로 주어진 User로부터 Relation의 from_user에 해당하는 RelatedManger를 사용
            # self.follow_realtions.get_or_create(to_user=user)

        # user로 주어진 User로부터 Relation의 to_user에 해당하는 RelatedManager를 사용
            # user.follow_relations.get_or_create(from_user=self)

    def unfollow(self, user):
        # 위의 반대 역할
        Relation.objects.filter(from_user=self, to_user=user).delete()

    def is_follow(self, user):
        # 이미 follow 상태면 unfollow하고 있는지 bool 여부를 반환
        # ModelManager.exists()를 사용
        # Relation을 검색하면 됨.
        return self.follow_relations.filter(to_user=user).exists()

    def is_follower(self, user):
        # 해당 유저가 나를 follow하고 있는지 bool여부를 반환
        return self.follower_relations.filter(from_user=user).exists()
        # return user.follow_relations.filter(to_user=self).exists()

    def follow_toggle(self, user):
        # 이미 follow상태면 unfollow, 아닐 경우 follow 상태로 만듬

        relation, relation_created = self.follow_relations.get_or_create(to_user=user)
        if not relation_created:
            relation.delete()
        else:
            return relation

    @property
    def following(self):
        relations = self.follow_relations.all()
        # __in은 쿼리셋 (?)
        return User.objects.filter(pk__in=relations.values('to_user'))

    @property
    def followers(self):
        relations = self.follower_relations.all()
        # __in은 쿼리셋 (?)
        return User.objects.filter(pk__in=relations.values('from_user'))



class Relation(models.Model):
    # 같은 중요도로 참조할 수 있어야 한다.
    from_user = models.ForeignKey(
        User,
        related_name="follow_relations"
        # User가 두 군데서 쓰이기 때문에 역참조가 필요. 여기다가 역참조(relate_name)을 쓰면 User에서 접근이 가능하다.
    )
    to_user = models.ForeignKey(
        User,
        related_name="follower_relations"  # 나를 팔로우하고 있는 사람들
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Relation from({}) to ({})'.format(
            self.from_user,
            self.to_user,
        )

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )

# 관계를 만드려면 Relation.objects.get_or_create(from_user="이철규", to_user="박보영")
    # 나를 팔로우하고 있는 사람을 보려면 자신이 from_user인 relation을 보면

    # 언팔로우
        # Relation.objects.filter(from_user="이한영", to_user="박보영").delete()

    # 역참조매니저
        # lhy.follow_relations.filter()와 Relation.objects.filter(from_user=lhy).filter()는 같은 의미
        # lhy.follower_relations.filter()는 Relation.objects.filter(from_user=lhy).filter()와 같은 의미

    # 팔로우 관계 만들기
        # lhy.follow_relations.create(to_user="박보영")
        # Relation.objects.create(from_user=lhy, to_user="박보영")은 같은 의미.


