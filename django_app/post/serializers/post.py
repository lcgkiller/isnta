from rest_framework import serializers

from ..models import Post

__all__ = (
    'PostSerializer',
)

# 일단 API View로 짠 뒤 -> 제네릭뷰로 바꾸는 연습을 할 것임
class PostSerializer(serializers.ModelSerializer):
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