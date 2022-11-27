from django.urls import path
from .views import UserLogin, UserLogout, UseRegister

urlpatterns = [
    path("login", UserLogin.as_view(), name='login'),
    path("logout", UserLogout.as_view(), name='logout'),
    path("register", UseRegister.as_view(), name='register'),
]