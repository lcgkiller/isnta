from django import forms
from django.core.exceptions import ValidationError

from ..models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'input-comment',
                    'placeholder': '댓글 입력',
                }
            )
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 3:
            raise ValidationError("세 글자 이상 입력하세요")
        return content