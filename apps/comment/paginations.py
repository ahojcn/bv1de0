from rest_framework.pagination import PageNumberPagination


class CommentPagination(PageNumberPagination):
    """
    获取用户列表的分页器
    """
    page_size = 12
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 12
