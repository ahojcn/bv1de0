from django.urls import path

from .views import User, VerifyCode, CsrfToken

urlpatterns = [
    # 用户注册
    path('UserRegister/', User.UserRegisterView.as_view(), name="user-register"),
    # 用户激活
    path('UserActive/<token>', User.UserActive.as_view(), name="user-active"),

    # 验证码
    path('VerifyCode/', VerifyCode.VerifyCode.as_view(), name="verify-code"),

    # 获取 csrftoken
    path('GetCsrfToken/', CsrfToken.CsrfTokenView.as_view(), name="get-csrftoken"),
]
