from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import PostSerializer
from ..models import Post, Comment

__all__ = (
    'PostListCreateView',
)


class PostListCreateView(APIView):
    # get요청이 왔을 때 Post.objects.all()을 PostSerializer를 통해  Response로 반환
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)  # 적절히 Json으로 바꿔준다.

    def post(self, request, *args, **kwargs):
        # serializer를 이용해 Post 인스턴스 생성
        # 해당 내용으로 Post 인스턴스의 my_comment 항목을 만들어준다.
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()로 생성된 Post Instance를 instance 변수에 할당
            instance = serializer.save(author=request.user)
            # comment_content에 request.data의 'comment'에  해당하는 값을 할당
            comment_content = request.data.get('comment')

            # 'comment'에 값이 온 경우 my_comment항목을 채워줌
            if comment_content:
                instance.my_comment = Comment.objects.create(
                    post=instance,
                    author=instance.author,
                    content=comment_content
                )
                instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)