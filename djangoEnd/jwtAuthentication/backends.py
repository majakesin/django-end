import jwt
from django.contrib.auth.models import User
from rest_framework import authentication
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None
        prefix, token = auth_data.decode('UTF-8').split()

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(username=payload['username'])
            return (user, token)

        except jwt.DecodeError as identifier:
            raise AuthenticationFailed('Your token is invalid. Please login. ')
        except jwt.ExpiredSignatureError as identifier:
            raise AuthenticationFailed('Your token is expired. Please login.')

        return super().authenticate(request)
