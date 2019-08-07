from django.middleware.csrf import get_token


def get_csrftoken(request):
    """
    获取csrftoken
    """
    csrftoken = get_token(request)
    return {'csrftoken': csrftoken}
