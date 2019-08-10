from rest_framework import serializers

from apps.comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    评论的序列化器
    """

    class Meta:
        model = Comment
        fields = "__all__"
