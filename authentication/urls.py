from django.urls import path
from .views import RegisterView, LoginView, UpdateUser, ChangePasswordView


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('update', UpdateUser.as_view()),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
]
