from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.Form):
    # SignupForm을 구성하고 해당 form을 view에서 사용하도록 설정
    username = forms.CharField(widget=forms.TextInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    # clean_<fieldname> 메서드를 사용해서 username 필드 유효성 검사

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "이미 존재하는 아이디입니다."
            )

        return username

    def clean_password2(self):
        # password1과 password2를 비교하여 같은지 비교
        # password2 필드에 clean_<fieldname>을 재정의한 이유는
        #   cleaned_data에 password1이 이미 들어와있어야 하기 때문
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "비밀번호가 일치하지 않습니다."
            )
        return password2

    def create_user(self):
        # 자신의 cleaned_data를 사용해서 유저를 생성

        user = User.objects.create(
            user=self.cleaned_data['username'],
            password=self.cleaned_data['password2']
        )
        return user
