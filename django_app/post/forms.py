from django import forms

from member.models import User


class ContactForm(forms.Form):
    user = forms.ModelChoiceField(
        label="작성자",
        queryset=User.objects.all(),
        required=True,
    )
    image = forms.ImageField(label="사진", required=True)

