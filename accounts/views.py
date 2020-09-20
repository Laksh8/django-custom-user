from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework import status
from rest_framework.response import Response
import requests
from .serializers import UserDetailsSerializer,StudentSerializer,TeacherSerializer,ResetPasswordSerializer
from django.conf import settings
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from .encrypt import encrypt_message,decrypt_message
from django.contrib.auth.hashers import check_password,make_password

def Authentication(request):
    if request.user.is_authenticated and "Bearer "+request.user.token == request.headers.get("Authorization"):
        return True
    return False

def Pagination(request,model):
    paginator = Paginator(model, 25)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


# Create your views here.
class LoginView(TokenObtainPairView):

    def post(self,request):
        token = super().post(request).data
        data = requests.post(settings.BASE_URL+"api/accounts/refresh/",token).json()
        user = User.objects.get(email=request.data.get("email"))
        user.token = data.get("access")
        user.save()
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class StudentListView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    def get(self,request):
        if not Authentication(request) or not request.user.is_teacher:
            print(request.user)
            return Response(["User Not Allowed"],status=status.HTTP_401_UNAUTHORIZED)

        users = Pagination(request,User.objects.filter(student=True))
        serializer = UserDetailsSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserListView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    def get(self,request):
        if not Authentication(request) or not request.user.is_teacher:
            return Response(["User Not Allowed"],status=status.HTTP_401_UNAUTHORIZED)

        # Add Page Number in get request ?page=
        users = Pagination(request,User.objects.filter((Q(student=True) | Q(teacher=True)) & Q(admin=False)))
        serializer = UserDetailsSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class StudentRegisterView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    def post(self,request):
        if not Authentication(request) or not request.user.is_teacher:
            return Response(["User Not Allowed"],status=status.HTTP_401_UNAUTHORIZED)

        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(["Created Successfully"],status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class TeacherRegisterView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    def post(self, request):
        if not Authentication(request) or not request.user.is_admin:
            return Response(["User Not Allowed"],status=status.HTTP_401_UNAUTHORIZED)

        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(["Created Successfully"], status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LogoutView(APIView):
    authentication_classes = [JWTAuthentication,SessionAuthentication]

    def get(self,request):
        print(request.headers)
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user.token = ""
            user.save()
            return Response(["User Logged Out"],status=status.HTTP_200_OK)
        return Response(["User Should Login First"],status=status.HTTP_401_UNAUTHORIZED)




class ForgotPasswordView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]


    def post(self,request):
        if request.data.get("email"):
            user = User.objects.filter(email=request.data.get("email")).first()
            if not user:
                return Response(["User of This email doesn't exist"],status=status.HTTP_400_BAD_REQUEST)
            print(encrypt_message(user.id))
            send_mail(
                "Reset Password Link",
                settings.BASE_URL+"api/accounts/reset-password/"+encrypt_message(user.id),
                settings.EMAIL_HOST_USER ,
                [request.data.get("email")],
                fail_silently=True,
            )
            return Response(["Reset Password Email Sent..."],status=status.HTTP_200_OK)

        return Response([
            {"error":"Email is required"}
        ],status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self,request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(id=decrypt_message(request.data.get("id"))).first()
            if user:
                user.password = make_password(serializer.data.get("password"))
                user.save()
                return Response(["Password Changed"],status=status.HTTP_200_OK)
            return Response(["Link is Not correct"],status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
