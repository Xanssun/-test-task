from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.serializers import (AuthSerializer, UserSerializer,
                             NewsSerializer, CommentSerializer)
from api.permissions import IsAdminUser
from users.models import CustomUser
from posts.models import News, Comment, Like
from rest_framework import status


class AuthViewSet(viewsets.ViewSet):
    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, token = serializer.save()
        return Response(token)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        author_username = self.request.data.get('author')
        author = CustomUser.objects.get(username=author_username)
        serializer.save(author=author)

    @action(methods=['post'], detail=True)
    def like(self, request, pk=None):
        news = self.get_object()
        user = self.request.user
        try:
            like = Like.objects.get(user=user, news=news)
            like.delete()
            news.likes_count -= 1
            news.save()
            return Response({'detail': 'Like removed.'},
                            status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            Like.objects.create(user=user, news=news)
            news.likes_count += 1
            news.save()
            return Response({'detail': 'Like added.'},
                            status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        news_id = self.kwargs['news_pk']
        news = get_object_or_404(News, pk=news_id)
        serializer.save(author=self.request.user, news=news)
