from rest_framework.routers import DefaultRouter

from api.views import AuthViewSet, CommentViewSet, NewsViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='users')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'news/(?P<news_pk>\d+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = router.urls
