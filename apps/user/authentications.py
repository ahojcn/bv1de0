from rest_framework import authentication
from rest_framework import exceptions

from apps.user.models import UserToken


class UserLoginAuthentication(authentication.BaseAuthentication):
    """
    用户是否登录验证
    """

    def authenticate_header(self, request):
        pass

    def authenticate(self, request):
        user_token = request.COOKIES.get('user_token')
        if user_token is None:
            raise exceptions.AuthenticationFailed('未登录')

        user_token_obj = UserToken.objects.filter(key=user_token).first()
        return user_token_obj.user, user_token_obj
