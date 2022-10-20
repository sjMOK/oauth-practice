from django.urls import path

from .views import naver_login, naver_callback


app_name = 'user'

urlpatterns = [
    path('/naver/login', naver_login),
    path('/naver/callback', naver_callback),
]
