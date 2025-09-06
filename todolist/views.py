from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .make_token import *
from rest_framework.authentication import TokenAuthentication

class LoginUser(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.validated_data['username'])
        token = get_tokens_for_user(user)
        return Response(data=token, status=status.HTTP_200_OK)

class TodolistView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses={200: TodolistSerializer(many=True)})
    def get(self, request):
        todolist = Todolist.objects.filter(user=request.user)
        serializer = TodolistSerializer(todolist, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=TodolistSerializer, responses={201: TodolistSerializer()})
    def post(self, request):
        serializer = TodolistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(request_body=TodolistSerializer, responses={201: TodolistSerializer()})
    def put(self, request, pk):
        todolist = get_object_or_404(Todolist, pk=pk, user=request.user)
        serializer = TodolistSerializer(todolist, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        todolist = get_object_or_404(Todolist, pk=pk, user=request.user)
        todolist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StaffRegister(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        User.objects.create_user(username=data['username'], password=data['password'])
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)