from rest_framework import serializers
from .models import Student, Teacher


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'username', 'password', 'email', 'motto', 'avatar', 'the_class']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        stu = Student(
            email=validated_data['email'],
            username=validated_data['username'],
            the_class=validated_data['the_class'],
            motto=validated_data['motto'],
            is_active=False,
        )

        try:
            validated_data['aaa']
        except KeyError as e:
            print('key error')

        stu.set_password(validated_data['password'])
        stu.save()
        return stu


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['username', 'motto', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}
