from rest_framework import serializers
from .models import Todolist, User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ "username", "email", "password"]
        read_only_fields = ["is_admin", "is_staff", "is_active"]
class TodolistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields = "__all__"
        read_only_fields = ["user"]  # user maydonini faqat o'qish uchun qilish 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Foydalanuvchini tekshirish
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "success": False,
                "detail": "User does not exist"
            })

        # Parolni tekshirish
        auth_user = authenticate(username=username, password=password)
        if auth_user is None:
            raise serializers.ValidationError({
                "success": False,
                "detail": "Username or password is invalid"
            })

        # Tekshiruvdan o'tgan userni attrs ichiga joylash
        attrs["user"] = auth_user
        return attrs    