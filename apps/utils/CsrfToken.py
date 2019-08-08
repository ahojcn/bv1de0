from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response


class CsrfTokenView(APIView):
    @csrf_exempt
    def post(self, request):
        csrftoken = get_token(request)
        return Response({'csrftoken': csrftoken})
