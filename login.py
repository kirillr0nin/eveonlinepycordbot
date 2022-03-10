from jwt import validate_eve_jwt
from ssoresponse import handle_sso_token_response
from authflow import print_auth_url
import json
import base64
import requests

def login(auth_code):
    with open('settings.json', 'r') as f:
            d = json.loads(f.read())
    client_id = d['settings'][0]["client_id"]
    client_secret = d['settings'][0]["client_secret"]
    user_pass = "{}:{}".format(client_id, client_secret)
    basic_auth = base64.urlsafe_b64encode(user_pass.encode('utf-8')).decode()
    auth_header = "Basic {}".format(basic_auth)

    headers = {
        "Authorization": auth_header,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'login.eveonline.com',
    }

    res = requests.post(
        "https://login.eveonline.com/v2/oauth/token",
        data= { "grant_type" : "authorization_code" , "code" : auth_code},
        headers=headers,
    )
    rev = handle_sso_token_response(res)
    return rev


