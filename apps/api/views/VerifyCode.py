from django.http.response import HttpResponse

from rest_framework.views import APIView

from apps.utils.GetVerifyCodeImage import get_verify_code_img


class VerifyCode(APIView):
    """
    获取验证码
    """

    def get(self, request):
        """
        :param request:
        :return:
        """
        # print(request.session['verify_code'])
        # print(request.session.get('verify_code'))
        img = get_verify_code_img(request)
        return HttpResponse(img, 'image/png')
