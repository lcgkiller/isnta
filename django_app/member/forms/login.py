from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '아이디를 입력하세요',
            }
        ), label="아이디"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요',
            }
        ), label="비밀번호")

    # is_valid를 실행했을 때, Form 내부의 모든 filed들에 대한 유효성을 검증하는 메서드
    def clean(self):
        # clean() 메서드를 실행하면 기본 결과 dict를 가져온다.
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(
            username=username,
            password=password,
        )

        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError(
                'Login credential not valid'
            )
        return self.cleaned_data
