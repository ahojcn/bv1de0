from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.utils.GetCsrfToken import get_csrftoken


class CsrfTokenView(APIView):
    @csrf_exempt
    def post(self, request):
        return Response(get_csrftoken(request))
