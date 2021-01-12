from django.urls import path
from django.contrib.auth.views import LogoutView as UserLogoutView

from accounts.views import UserLoginView, UserSignupView

app_name ="accounts"

urlpatterns = [
    path("login", UserLoginView.as_view(), name="login"),
    path("signup", UserSignupView.as_view(), name="signup"),
    path("logout", UserLogoutView.as_view(), name="logout"),
]
