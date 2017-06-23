from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.db import models

from utils.fields import CustomImageField


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

