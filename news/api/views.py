from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import AuthSerializer, UserSerializer, NewsSerializer, CommentSerializer
from api.permissions import IsObjectOwnerOrAdmin, IsAdminUser
from users.models import CustomUser

from posts.models import News, Comment, Like


class AuthView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, token = serializer.save()
        return Response(token)


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsList(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        for item in data:
            news_id = item['id']
            item['comments_count'] = Comment.objects.filter(news_id=news_id).count()
            item['likes_count'] = Like.objects.filter(news_id=news_id).count()
        return response

    def perform_create(self, serializer):
        author_username = self.request.data.get('author')
        author = CustomUser.objects.get(username=author_username)
        serializer.save(author=author)

class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsObjectOwnerOrAdmin | IsAdminUser]


class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        news_id = self.kwargs['pk']
        news = get_object_or_404(News, pk=news_id)
        serializer.save(author=self.request.user, news=news)


class CommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsObjectOwnerOrAdmin | IsAdminUser]


class LikeToggle(generics.GenericAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        news = self.get_object()
        user = self.request.user
        try:
            like = Like.objects.get(user=user, news=news)
            like.delete()
            news.likes_count -= 1
            news.save()
            return Response({'detail': 'Like removed.'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            Like.objects.create(user=user, news=news)
            news.likes_count += 1
            news.save()
            return Response({'detail': 'Like added.'}, status=status.HTTP_201_CREATED)
