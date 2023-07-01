from django.urls import path, include

from .views import UserView, UserRegisterView, LoginView
from knox.views import LogoutView

urlpatterns = [
    path('profile', UserView.as_view(), name='profile'),
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
