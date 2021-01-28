from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,StudentRegisterView,TeacherRegisterView,StudentListView,UserListView,LogoutView,
    ForgotPasswordView,ResetPasswordView,GeneralAuthView
)


urlpatterns = [
    path("refresh/",TokenRefreshView.as_view()),
    path("login/",LoginView.as_view()),
    path("logout/",LogoutView.as_view()),
    path("student-register/",StudentRegisterView.as_view()),
    path("teacher-register/",TeacherRegisterView.as_view()),
    path("student-list/",StudentListView.as_view()),
    path("user-list/",UserListView.as_view()),
    path("forgot-password/",ForgotPasswordView.as_view()),
    path("reset-password/",ResetPasswordView.as_view()),
    path("",GeneralAuthView.as_view())
]
