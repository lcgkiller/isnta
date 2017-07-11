from rest_framework import status, permissions, generics

from member.serializers import UserSerializer
from member.serializers.user import UserCreationSerializer
from post.serializers import PostSerializer
from utils.permissions import ObjectIsRequestUser
from ..models import User

__all__ = (
    'UserRetrieveUpdateDestroyView',
    'UserListCreateView',
)


# 제네릭 API view는 get_object가 이미 정의되어 있음.
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()  # 객체 하나를 가져와야 한다. 그런데 all()로 가져옴. 제네릭API뷰가 특정 오브젝트를 하나 들고온다.
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,  # 쿼리셋 자체가 유저기 때문에 유저 자체를 비교해야 함
    )

    # 삭제도 유저 자기 자신만

    # @staticmethod
    # def get_object(pk):
    #     try:
    #         return User.objects.get(pk=pk)
    #     except User.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    # # retrieve
    # def get(self, request, pk):
    #     user = self.get_object(pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)
    #
    # # update
    # def put(self, request, pk):
    #     user = self.get_object(pk)
    #     serializer = UserSerializer(user, request, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # # partial update
    # def patch(self, request, pk):
    #     user = self.get_object(pk)
    #     serializer = UserSerializer(user, request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, reuqest, pk):
    #     user = self.get_object(pk)
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# (중간미션) 이후 UserListCreateView를 구현 후 urls_apis.py에 연결 (generics.List
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer
