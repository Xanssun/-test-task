from rest_framework import authentication
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return None

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None

        if not user.check_password(password):
            return None

        token = self.generate_token(user)
        return (user, token)

    def generate_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
