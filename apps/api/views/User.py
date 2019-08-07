import re

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader

from rest_framework.views import APIView
from rest_framework.response import Response

from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired

from apps.user.models import User


class UserRegisterView(APIView):
    """
    用户注册接口
    """

    def __init__(self, *args, **kwargs):
        self._res_data = {"status_code": -2, "err_msg": None, "data": None}
        super().__init__(*args, **kwargs)

    def post(self, request):
        username = request.data.get("username")
        pwd = request.data.get("pwd")
        cpwd = request.data.get("cpwd")
        email = request.data.get("email")
        verify_code = request.data.get("verify_code")

        # 数据完整性校验
        if not all([username, pwd, cpwd, email, verify_code]):
            self._res_data["status_code"] = -1
            self._res_data["err_msg"] = "数据不完整"
            return Response(self._res_data)

        # 校验数据正确性
        if verify_code.upper() != request.session.get('verify_code').upper():
            self._res_data["status_code"] = -1
            self._res_data["err_msg"] = "验证码有误"
            return Response(self._res_data)

        user_obj = authenticate(username=username)
        if user_obj is not None:
            self._res_data["status_code"] = -1
            self._res_data["err_msg"] = "用户已存在"
            return Response(self._res_data)

        if pwd != cpwd:
            self._res_data["status_code"] = -1
            self._res_data["err_msg"] = "两次输入的密码不一致"
            return Response(self._res_data)

        if not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            self._res_data["status_code"] = -1
            self._res_data["err_msg"] = "邮箱格式有误"
            return Response(self._res_data)

        # 创建未激活用户
        user_obj = None
        try:
            user_obj = User.objects.create_user(username=username, password=pwd, email=email)
            user_obj.is_active = False
            user_obj.save()
        except Exception as e:
            self._res_data["status_code"] = -1
            self._res_data["err_msg"] = "用户已存在"
            return Response(self._res_data)

        # 生成激活 token，设置过期时间
        s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 60 * 60 * 24)
        info = {'confirm': user_obj.id}
        token = s.dumps(info)  # typeof token = bytes
        token = token.decode('utf8')

        active_url = 'http://127.0.0.1:8000/api/UserActive/' + token

        # 发送激活邮件
        template = loader.get_template('EmailTemplate.html')
        html = template.render({'username': username, 'email': email, 'active_url': active_url})
        send_mail('注册激活', '', settings.EMAIL_FROM, [email], html_message=html)

        self._res_data["status_code"] = 0
        self._res_data["data"] = {
            "username": user_obj.username,
            "last_login": user_obj.last_login,
            "is_active": user_obj.is_active,
            "nick_name": user_obj.nick_name,
            "avatar": settings.STATIC_URL + "default_avatar.png",
        }
        return Response(self._res_data)


class UserActive(APIView):
    """
    用户激活接口
    """

    def __init__(self, *args, **kwargs):
        self._res_data = {"status_code": -2, "err_msg": None, "data": None}
        super().__init__(*args, **kwargs)

    def get(self, request, token):
        s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        try:
            info = s.loads(token)
            # 获取待激活用户的 id
            user_id = info['confirm']
            # 获取用户信息，并激活
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()

            self._res_data["status_code"] = 0
            self._res_data["data"] = {
                "username": user.username,
                "last_login": user.last_login,
                "is_active": user.is_active,
                "nick_name": user.nick_name,
                "avatar": settings.STATIC_URL + "default_avatar.png",
            }
            return Response(self._res_data)
        except SignatureExpired:
            # 激活链接过期
            self._res_data["status_code"] = -1
            self._res_data["err_msg"] = "激活链接已过期"
            return Response(self._res_data)
        except Exception:
            self._res_data["status_code"] = -1
            self._res_data["err_msg"] = "未知错误"
            return Response(self._res_data)
