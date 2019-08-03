from django.shortcuts import render

# Create your views here.
# from rest_framework.response import Response
# from rest_framework import status

from rest_framework import generics
from .serializers import StudentSerializer, TeacherSerializer
from .models import Student, Teacher


class StudentList(generics.ListCreateAPIView):
    """
    学生列表接口

    1. get 获取所有学生
    2. post 注册一个学生
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetail(generics.RetrieveUpdateAPIView):
    """
    学生详情接口

    1. put 更新用户信息
    2. get 获取用户信息
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
