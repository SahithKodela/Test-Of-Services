"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from reg.views import login,reg,Pro_User,SerializerUser, SerializerReg, otp_gen, otp_ver, UserupdateAPI, UserRetrieveAPIView, UserUpdateAPIView, UserdestroyAPI,SampleOtpver, UserCreateAPIView, SampleOtpGen
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'user',SerializerUser)
router.register(r'reg_api',SerializerReg)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login),
    url(r'^otp_gen/', otp_gen),
    url(r'^otp_ver/', otp_ver),
url(r'^SampleOtpGen/', SampleOtpGen.as_view()),
url(r'^SampleOtpver/', SampleOtpver.as_view()),

    url(r'^reg/',reg),
    url(r'^pro_user/',Pro_User.as_view()),
    url(r'',include(router.urls)),
    url(r'post/', UserCreateAPIView.as_view()),
    url(r'register/', UserupdateAPI.as_view()),
    url(r'^(?P<user>[\w-]+)/$', UserRetrieveAPIView.as_view()),
    url(r'^(?P<user>[\w-]+)/update$', UserUpdateAPIView.as_view()),
    url(r'^(?P<user>[\w-]+)/destroy', UserdestroyAPI.as_view()),

]
