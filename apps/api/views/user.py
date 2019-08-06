from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class UserRegisterView(APIView):
    """
    用户注册接口
    """

    def post(self, request):
        print(request.data)
        return Response("ok...")
