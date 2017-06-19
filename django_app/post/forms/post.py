from django import forms
from ..models import Post, Comment


class PostForm(forms.ModelForm):

    # 생성자를 조작해서 실제 Post의 photo필드는 blank=True
    #   (Form에서 required=False)이지만, Form을 사용할때는 반드시 photo를 받도록 required=True) 한다.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True

        # 글 작성할 때 comment를 달았으면 초기값으로 정해준다.
        if self.instance.my_comment:
            self.fields['comment'].initial = self.instance.my_comment.content

    comment = forms.CharField(
        required=False,
        widget=forms.TextInput
    )

    class Meta:
        model = Post
        fields = (
            'photo',
            'comment',
        )

    def save(self, **kwargs):

        # 전달된 키워드인자 중 'commit'키 값을 가져옴
        commit = kwargs.get('commit', True)
        # author가 없을 경우 None을 가진다.
        author = kwargs.pop('author', None)

        # super()의 save() 호출
        self.instance.author = author
        instance = super().save(**kwargs)

        # commit 인수가 True이며 comment필드가 채워져 있을 경우 Comment생성 로직을 진행
        # 해당 Comment는 instacne의 my_comment필드를 채워준다.
        #   이 위에서 super().save()를 실행하기 때문에 현재 위치에서는 author나 pk에 대한 검증이 끝난 상태임
        comment_string = self.cleaned_data['comment']

        if commit and comment_string:
            # my_comment가 있는 경우 (update 상황에 해당)
            if instance.my_comment:
                instance.my_comment.content = comment_string
                instance.my_comment.save()
            # my_comment가 없는 경우 (Comment객체를 생성해 my_comment OTO field에 할당)
            else:
                instance.my_comment = Comment.objects.create(
                    post=instance,
                    author=author,
                    content=comment_string,
                )
            instance.save()
        # ModelForm의 save()에서 반환해야 하는 model의 인스턴스를 리턴
        return instance