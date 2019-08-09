import re
import uuid

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader

from rest_framework import views, viewsets
from rest_framework.response import Response

from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired

from apps.user.models import User, UserToken
from apps.user.serializers import UserSerializer
from apps.user.authentications import UserLoginAuthentication


class UserRegisterView(views.APIView):
    """
    用户注册接口
    """

    def __init__(self, **kwargs):
        self._res_data = {"status_code": -2, "msg": None, "data": None}
        super().__init__(**kwargs)

    def post(self, request):
        username = request.data.get("username")
        pwd = request.data.get("pwd")
        cpwd = request.data.get("cpwd")
        email = request.data.get("email")
        verify_code = request.data.get("verify_code")

        # 数据完整性校验
        if not all([username, pwd, cpwd, email, verify_code]):
            self._res_data["status_code"] = -1
            self._res_data["msg"] = "数据不完整"
            return Response(self._res_data)

        # 校验数据正确性
        if verify_code.upper() != request.session.get('verify_code', default="").upper():
            self._res_data["status_code"] = -1
            self._res_data["msg"] = "验证码有误"
            return Response(self._res_data)

        user_obj = authenticate(username=username)
        if user_obj is not None:
            self._res_data["status_code"] = -1
            self._res_data["msg"] = "用户已存在"
            return Response(self._res_data)

        if pwd != cpwd:
            self._res_data["status_code"] = -1
            self._res_data["msg"] = "两次输入的密码不一致"
            return Response(self._res_data)

        if not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            self._res_data["status_code"] = -1
            self._res_data["msg"] = "邮箱格式有误"
            return Response(self._res_data)

        # 创建未激活用户
        user_obj = None
        try:
            user_obj = User.objects.create_user(username=username, password=pwd, email=email)
            user_obj.is_active = False
            user_obj.save()
        except Exception as e:
            self._res_data["status_code"] = -1
            self._res_data["msg"] = "用户已存在"
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
        self._res_data["msg"] = "注册成功，已发送激活邮件"
        self._res_data["data"] = {
            "username": user_obj.username,
            "last_login": user_obj.last_login,
            "is_active": user_obj.is_active,
            "nick_name": user_obj.nick_name,
            "avatar": settings.STATIC_URL + "default_avatar.png",
        }
        return Response(self._res_data)


class UserActiveView(views.APIView):
    """
    用户激活接口
    """

    def __init__(self, **kwargs):
        self._res_data = {"status_code": -2, "msg": None, "data": None}
        super().__init__(**kwargs)

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
            self._res_data["msg"] = user.username + "激活成功"
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
            self._res_data["msg"] = "激活链接已过期"
            return Response(self._res_data)
        except Exception:
            self._res_data["status_code"] = -1
            self._res_data["msg"] = "未知错误"
            return Response(self._res_data)


class UserLoginView(views.APIView):
    """
    用户登录接口
    """

    def __init__(self, **kwargs):
        self._res_data = {"status_code": -2, "msg": None, "data": None}
        super().__init__(**kwargs)

    def post(self, request):
        # 获取数据
        username = request.data.get('username')
        pwd = request.data.get('pwd')
        verify_code = request.data.get("verify_code")

        # 校验数据
        if not all([username, pwd, verify_code]):
            self._res_data["status_code"] = -1
            self._res_data["msg"] = "数据不完整"
            return Response(self._res_data)

        if verify_code.upper() != request.session.get('verify_code', default="").upper():
            self._res_data["status_code"] = -1
            self._res_data["msg"] = "验证码有误"
            return Response(self._res_data)

        user_obj = authenticate(username=username, password=pwd)
        if user_obj is None:
            # 没有该用户
            self._res_data["status_code"] = -1
            self._res_data["msg"] = "用户名或密码错误"
            return Response(self._res_data)

        # 生成或更新 用户相关的 token
        random_str = str(uuid.uuid4())
        UserToken.objects.update_or_create(user=user_obj, defaults={"key": random_str})

        self._res_data["status_code"] = 0
        self._res_data["msg"] = "登录成功"
        self._res_data["data"] = {
            "username": user_obj.username,
            "avatar": settings.STATIC_URL + "default_avatar.png",
            "is_active": user_obj.is_active,
            "last_login": user_obj.last_login,
            "nick_name": user_obj.nick_name,
        }

        resp = Response(self._res_data)
        resp.set_cookie('user_token', random_str)
        return resp


class UserHomeView(viewsets.ModelViewSet):
    """
    个人中心信息
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [UserLoginAuthentication]
