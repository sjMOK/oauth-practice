from django.shortcuts import redirect
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

import requests
import urllib

from .models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_or_create_user(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        random_password = User.objects.make_random_password()
        user = User.objects.create_user(email=email, password=random_password)

    return user


def naver_login(request):
    client_id = getattr(settings, 'OAUTH_NAVER_CLIENT_ID')
    rediret_uri = getattr(settings, 'OAUTH_NAVER_REDIRECT_URI')
    encoded_redirect_uri = urllib.parse.quote(rediret_uri)

    return redirect(f'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={encoded_redirect_uri}&state=test')


@api_view(['GET'])
def naver_callback(request):
    client_id = getattr(settings, 'OAUTH_NAVER_CLIENT_ID')
    client_secret = getattr(settings, 'OAUTH_NAVER_CLIENT_SECRET')
    authorization_code = request.query_params['code']

    token_response = requests.get(f'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={authorization_code}&state=test')
    access_token = token_response.json()['access_token']

    headers = {'Authorization': f'Bearer {access_token}'}
    userinfo_response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
    userinfo_data = userinfo_response.json()['response']
    email = userinfo_data['email']

    user = get_or_create_user(email)

    return Response(get_tokens_for_user(user))


def google_login(request):
    client_id = getattr(settings, 'OAUTH_GOOGLE_CLIENT_ID')
    redirect_uri = getattr(settings, 'OAUTH_GOOGLE_REDIRECT_URI')
    scope = 'https://www.googleapis.com/auth/userinfo.email'

    encoded_redirect_uri = urllib.parse.quote(redirect_uri)
    encoded_scope = urllib.parse.quote(scope)
    
    return redirect(
        f'https://accounts.google.com/o/oauth2/v2/auth?scope={encoded_scope}&access_type=offline&response_type=code&state=test&redirect_uri={encoded_redirect_uri}&client_id={client_id}'
    )


@api_view(['GET'])
def google_callback(request):
    client_id = getattr(settings, 'OAUTH_GOOGLE_CLIENT_ID')
    client_secret = getattr(settings, 'OAUTH_GOOGLE_CLIENT_SECRET')
    redirect_uri = getattr(settings, 'OAUTH_GOOGLE_REDIRECT_URI')
    authorization_code = request.query_params['code']

    encoded_redirect_uri = urllib.parse.quote(redirect_uri)

    token_response = requests.post(f'https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={authorization_code}&grant_type=authorization_code&redirect_uri={encoded_redirect_uri}')
    access_token = token_response.json()['access_token']

    headers = {'Authorization': f'Bearer {access_token}'}
    userinfo_response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
    email = userinfo_response.json()['email']

    user = get_or_create_user(email)

    return Response(get_tokens_for_user(user))
