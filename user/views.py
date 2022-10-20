from django.shortcuts import redirect
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests
import urllib


@api_view(['GET'])
def naver_login(request):
    client_id = getattr(settings, 'OAUTH_NAVER_CLIENT_ID')
    rediret_url = 'http://127.0.0.1:8000/user/naver/callback'
    encoded_redirect_url = urllib.parse.quote(rediret_url)

    return redirect(f'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={encoded_redirect_url}&state=test')


@api_view(['GET'])
def naver_callback(request):
    print(request.query_params['code'])
    client_id = getattr(settings, 'OAUTH_NAVER_CLIENT_ID')
    client_secret = getattr(settings, 'OAUTH_NAVER_CLIENT_SECRET')
    code = request.query_params['code']

    token_response = requests.get(f'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state=test')
    access_token = token_response.json()['access_token']

    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
    profile_data = profile_response.json()

    return Response(profile_data)
