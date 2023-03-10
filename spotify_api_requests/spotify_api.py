#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import base64
import json
import requests
import sys

# Workaround to support both python 2 & 3
try:
    import urllib.request, urllib.error
    import urllib.parse as urllibparse
except ImportError:
    import urllib as urllibparse


# ----------------- 0. SPOTIFY BASE URL ----------------

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# ----------------- 1. USER AUTHORIZATION ----------------

# spotify endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')


# client keys
CLIENT_ID = '5314b537e3f04cbfb3a9a3b4a5deb8e8'
CLIENT_SECRET = 'ca09e9507159477da5755a19b721af5b'


# server side parameter
# * fell free to change it if you want to, but make sure to change in
# your spotify dev account as well *
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8081
#REDIRECT_URI = "{}:{}/callback/".format(CLIENT_SIDE_URL, PORT)
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = [
    'user-read-private',
    'playlist-read-private',
    'playlist-modify-public',
    'playlist-modify-private',
    'user-library-read',
    'user-library-modify',
    'user-follow-read',
    'user-follow-modify'
]
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

# https://developer.spotify.com/web-api/authorization-guide/
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": ' '.join(SCOPE),
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val)) 
                     for key, val in list(auth_query_parameters.items())])

AUTH_URL = "{}/?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)




def authorize(auth_token):

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }

    #python 3 or above
    if sys.version_info[0] >= 3:
        base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
        headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    else:
        base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
        headers = {"Authorization": "Basic {}".format(base64encoded)}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header

