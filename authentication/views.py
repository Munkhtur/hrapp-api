from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, UserUpdateSerializer, ChangePasswordSerializer
from django.contrib import auth
from rest_framework.permissions import IsAuthenticated
import jwt
from django.contrib.auth import get_user_model
from .backends import UserBackEnds
import datetime
# from .models import User
# Create your views here.


User = get_user_model()


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        email = data.get("email", '')
        password = data.get("password", '')
        # user = User.objects.get(email=email)
        # is_valid = user.check_password(password)
        back = UserBackEnds()
        user = back.authenticate(email=email, password=password)
        # user = auth.authenticate(email=email, password=password)
        send_mail(
            "Password Reset for {title}".format(title="Some website title"),
            "klajsdnflakjfak",
            "noreply@somehost.local",
            ["gmunkhtur@gmail.com"],
            fail_silently=False,
        )

        def send_email():
            msg = EmailMessage('Request Callback',
                               'Here is the message.', "gmunkhtur@gmail.com", to=['gmunkhtur@gmail.com'])
            msg.send()
        send_email()
        if user:
            auth_token = jwt.encode(
                {"email": user.email, "password": password, "exp": datetime.datetime.now(datetime.timezone.utc).astimezone() + datetime.timedelta(hours=24)}, settings.JWT_SECRET_KEY)

            serializer = UserSerializer(user)

            data = {
                "user": serializer.data, 'token': auth_token
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateUser(UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def post(self, request):
        data = request.data
        email = data.get("email", '')
        print(data)
        print(data, ">>>>>>>>>>>>>>>>>>>>>data")
        print(email, ">>>>>>>>>>>>>>>>>>>>>>")
        user = User.objects.get(email=email)
        # newObj = {**data, "password": "admin"}
        # print(newObj)
        # print(password, "password -------------------------")
        serializer = UserUpdateSerializer(instance=user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
