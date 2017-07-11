from rest_framework import serializers
from ..models import User

__all__ = (
    'UserSerializer',
    'UserCreationSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'nickname'
        )

        # serializers의 __init__ 파일 구현
        # urls에 urls_apis, urls_views로 파일 구분
        # apis에 user.py 모듈 생성, UserRetrieveUpdateDestroyView 구현
        # urls.urls_apis에 UserRetrieveUpdateDestroyView.as_view()를 연결
        # config.urls.urls_apis에 member.urls.urls_apis를 연결


class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=50,
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("중복되는 아이디가 존재합니다.")
        return username

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 서로 일치하지 않습니다.')
        return data

    def save(self, *args, **wargs):
        user = User.objects.create_user(
            username=self.validated_data.get('username', ''),
            password=self.validated_data.get('password1', ''),
        )
        return user
