from django.urls import path

from .views import naver_login, naver_callback, google_login, google_callback


app_name = 'user'

urlpatterns = [
    path('/naver/login', naver_login),
    path('/naver/callback', naver_callback),
    path('/google/login', google_login),
    path('/google/callback', google_callback),
]
