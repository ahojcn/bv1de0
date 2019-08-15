from rest_framework import viewsets, filters

from apps.comment.models import (
    Comment
)
from apps.comment.serializers import CommentSerializer
from apps.comment.paginations import CommentPagination


class CommentViewSet(viewsets.ModelViewSet):
    """
    评论视图
    """

    queryset = Comment.objects.all().order_by('-add_time')
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('video_to__id',)
