from django.shortcuts import render

# Create your views here.
# from rest_framework.response import Response
# from rest_framework import status


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re

from .models import Student, Teacher


class StudentLC(APIView):
    """
    学生 list and create
    """

    def get(self, request):
        """list"""
        ret_list = list()

        for stu in Student.objects.all():
            tmp = {
                'id': stu.id,
                'username': stu.username,
                'avatar': str(stu.avatar),
                'motto': stu.motto,
                'email': stu.email,
                'is_active': stu.is_active,
                'date_joined': stu.date_joined,
                'last_login': stu.last_login,
                'first_name': stu.first_name,
                'last_name': stu.last_login
            }
            ret_list.append(tmp)

        return Response(ret_list, status=200)

    def post(self, request):
        """create"""
        return Response('ok')
