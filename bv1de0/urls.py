"""bv1de0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('users/', include('apps.users.urls')),  # 用户
    path('msgboard/', include('apps.msgboard.urls')),  # 留言
    path('video/', include('apps.video.urls')),  # 视频
    path('bclass/', include('apps.bclass.urls')),  # 班级

    path('media/<path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
