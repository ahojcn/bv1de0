from django.contrib import admin
from django.urls import path, include

from apps.utils import CsrfToken, VerifyCode

urlpatterns = [
    path('admin/', admin.site.urls),

    # 用户相关
    path('apis/user/', include('apps.user.urls')),

    # 视频相关
    path('apis/video/', include('apps.video.urls')),

    # 评论相关
    path('apis/comment/', include('apps.comment.urls')),

    # 其他
    path('apis/csrftoken/', CsrfToken.CsrfTokenView.as_view(), name="csrftoken"),
    path('apis/verifycode/', VerifyCode.VerifyCodeView.as_view(), name="verifycode"),
]
