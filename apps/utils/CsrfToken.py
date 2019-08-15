from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response


class CsrfTokenView(APIView):
    """
    获取
    """

    def __init__(self, **kwargs):
        self._res_data = {"status_code": -2, "msg": None}
        super().__init__(**kwargs)

    @csrf_exempt
    def post(self, request):
        self._res_data["status_code"] = 0
        self._res_data["msg"] = "ok"
        resp = Response(self._res_data)
        resp.set_cookie('csrftoken', get_token(request))
        return resp
