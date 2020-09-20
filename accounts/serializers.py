from rest_framework import serializers
from accounts.models import User

#Serializers Goes here...
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',"password"]

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",'email',"token","phone","name","image"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',"name","phone","image","password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            name= validated_data.get("name"),
            email=validated_data.get("email"),
            password=validated_data.get("password"),
            phone=validated_data.get("phone"),
            image= validated_data.get("image"),
        )
        return user


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',"name","phone","image","password"]

    def create(self, validated_data):
        user = User.objects.create_teacher(
            name= validated_data.get("name"),
            email=validated_data.get("email"),
            password=validated_data.get("password"),
            phone=validated_data.get("phone"),
            image= validated_data.get("image"),
        )
        return user


class ResetPasswordSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=500)
    password = serializers.CharField(max_length=500)