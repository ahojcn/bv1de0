from rest_framework.pagination import PageNumberPagination


class VideoListPagination(PageNumberPagination):
    """
    获取视频列表的分页器
    """
    page_size = 12
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 12
