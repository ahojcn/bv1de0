from rest_framework import serializers

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nick_name', 'avatar', 'motto', 'is_active', 'password']
        read_only_fields = ['id', 'email', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.nick_name = validated_data.get('nick_name', instance.nick_name)
        instance.motto = validated_data.get('motto', instance.motto)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance
