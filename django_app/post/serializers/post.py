from rest_framework import serializers

from member.serializers import UserSerializer
from ..serializers.comment import CommentSerializer
from ..models import Post

__all__ = (
    'PostSerializer',
)

# 일단 API View로 짠 뒤 -> 제네릭뷰로 바꾸는 연습을 할 것임

class PostSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    my_comment = CommentSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'my_comment',
        )
        read_only_fields = (
            'author',
            'my_comment',
        )