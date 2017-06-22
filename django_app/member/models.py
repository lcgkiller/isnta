from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.db import models


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

    def __str__(self):
        return self.nickname or self.username

