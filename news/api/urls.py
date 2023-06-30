from django.urls import path
from api.views import AuthView, CreateUserView
from api.views import CommentCreate, CommentDelete, LikeToggle, NewsDetail, NewsList

app_name = 'api'

urlpatterns = [
    path('auth/', AuthView.as_view(), name='auth'),
    path('users/', CreateUserView.as_view(), name='create_user'),
    path('news/', NewsList.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),
    path('news/<int:pk>/comments/', CommentCreate.as_view(), name='comment-create'),
    path('comments/<int:pk>/', CommentDelete.as_view(), name='comment-delete'),
    path('news/<int:pk>/like/', LikeToggle.as_view(), name='like-toggle'),
]
