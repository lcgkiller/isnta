from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class FacebookBackend:

    # 예전에는 로그인을 하기전에 authenticate를 거쳤어야 함. facebook_id가 있는지 검사하는 기능
    # 지금은 반드시 필요한 것은 아니다.
    def authenticate(self, request, facebook_id):
        username = '{}_{}_{}'.format(
            self.model.USER_TYPE_FACEBOOK,
            settings.FACEBOOK_APP_ID,
            facebook_id,
        )
        try:
            user = User.objects.get(
                user_type=User.USER_TYPE_FACEBOOK,
                username=username
            )
            return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):

        try:
            return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return None


