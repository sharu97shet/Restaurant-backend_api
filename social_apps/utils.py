import requests
from google.auth.transport import requests
from google.oauth2 import id_token
from apiuser.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime
from requests import get, post, put

class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info=id_token.verify_oauth2_token(access_token, requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                return id_info
        except:
            return "the token is either invalid or has expired"


def register_social_user(provider, email, first_name, last_name):
    print("provide",provider)
    old_user=User.objects.filter(email=email)
    if old_user.exists():
        if provider == old_user[0].auth_provider:
            #register_user=authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)

            return {
                'full_name':old_user[0].get_full_name,
                'email':old_user[0].email,
                'tokens':old_user[0].tokens()
            }
        else:
            raise AuthenticationFailed(
                detail=f"please continue your login with {old_user[0].auth_provider}"
            )
    else:
        new_user={
            'email':email,
            'first_name':first_name,
            'last_name':last_name,
            'password':settings.SOCIAL_AUTH_PASSWORD,
            'birth_day':datetime(1970, 1, 1)
        }
        user=User.objects.create_user(**new_user)
        user.auth_provider=provider
        user.is_verified=True
        #user.birth_day=None
        user.save()
        login_user=authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
       
        tokens=login_user.tokens()
        print('tokens', tokens)
        return {
            'email':login_user.email,
            'full_name':login_user.get_full_name,
            "access_token":str(tokens.get('access')),
            "refresh_token":str(tokens.get('refresh'))
        }