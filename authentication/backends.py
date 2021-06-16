import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
# from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        print(request, "fdkjhjlkjhlh")
        auth_data = authentication.get_authorization_header(request)
        print(auth_data, 'auth_data')
        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms="HS256")
            print(payload, "pay;oad backends")

            user = User.objects.get(email=payload['email'])

            return (user, token)
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Expired token')

        return super().authenticate(request)


class UserBackEnds(ModelBackend):
    def authenticate(self, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        try:
            user = User.objects.get(email=email)
            print(user, 'userbackends')
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            pass
