from rest_framework import serializers

from apps.comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    评论的序列化器
    """

    class Meta:
        model = Comment
        fields = ["id", "detail", "add_time", "user_info", "video_to"]

    user_info = serializers.SerializerMethodField()

    def get_user_info(self, com_obj):
        user_info = {
            "username": com_obj.user.username,
            "avatar": com_obj.user.avatar.url
        }
        return user_info
