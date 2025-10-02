from django.contrib.auth.views import LoginView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, logout_view

app_name = UsersConfig.name

urlpatterns = [
    path(
        "",
        LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
