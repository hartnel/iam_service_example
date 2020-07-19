from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.http.response import JsonResponse
from rest_framework.exceptions import *
from keycloak.exceptions import KeycloakInvalidTokenError, KeycloakError
from keycloak import KeycloakOpenID
from aaa_services.middleware import REDIRECT_URL, MAX_TIME, SPLIT
from django.conf import settings

import base64

from datetime import datetime , date
from aaa_services import keycloak_web
from django.urls import reverse
from django.conf import settings

INIT_VIEW = settings.INIT_VIEW

def convert_time(timedelta_):
    days = timedelta_.days
    hours, remainder = divmod(timedelta_.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    # If you want to take into account fractions of a second
    seconds += timedelta_.microseconds / 1e6
    total_seconds = seconds + minutes*60 + hours*60*60 + days*24*60*60
    total_minutes = total_seconds/60
    total_hours   = total_minutes/60
    total_days    = total_hours/24
    return total_seconds, total_minutes, total_hours, total_days

def check_request(params):
    init_ = params.get("init", "")
    return init_


def url_parser(url , params : dict):
    keys = params.keys()
    new_url = url
    if len(keys):
        new_url += "?"
        for key in keys:
            if type(params[key]) == list:
                new_url += key + "=" + params[key][0] + "&"
            else:
                new_url += key + "=" + params[key] + "&"
    return new_url

def home(request):

    params = request.GET.copy()

    token = params.get('token', None)

    to = request.build_absolute_uri()

    params['goto'] = to

    print("params de la requete" ,  params)

    if not token:
        return redirect(to=url_parser(REDIRECT_URL , params), permanent=True)

    else:
        token = base64.b64decode(token).decode('ascii')
        # _, time, _, _ = convert_time(
        #             timedelta_ = datetime.now() - date.fromisoformat(
        #                                             token.split(SPLIT)[1]
        #                                         )
        #            )
        time = 1
        if time > MAX_TIME:
            return JsonResponse({"detail": AuthenticationFailed.default_detail},
                                        status=AuthenticationFailed.status_code)
        else:
            init_token = params.get('init', None)

            if not init_token:
                return JsonResponse({"detail": AuthenticationFailed.default_detail},
                                        status=AuthenticationFailed.status_code)
            else:
               
                try:
                    init_token = init_token.split('?init=')[0]
                    print("init token envoyé à keycloak" ,  init_token)
                    user = keycloak_web.userinfo(init_token)
                    params['username'] = user['name']
                    params['init'] = init_token

                    return redirect(url_parser(INIT_VIEW , params))

                except KeycloakError as e:
                    print(e , "Keycloak error je te dis ok  moi c est ok ")
                    return JsonResponse({"detail": AuthenticationFailed.default_detail},
                                        status=AuthenticationFailed.status_code)

def home1(request):
    print(request.META)
    
    params = request.GET.copy()

    print(params, "===========")
    init_ = check_request(params = params)
    print(init_)

    return HttpResponse("Bonjour, tout s'est bien passé")
