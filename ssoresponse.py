from jwt import validate_eve_jwt
import requests
import urllib
import json

def handle_sso_token_response(sso_response):
    """Handles the authorization code response from the EVE SSO.
    Args:
        sso_response: A requests Response object gotten by calling the EVE
                      SSO /v2/oauth/token endpoint
    """

    if sso_response.status_code == 200:
        data = sso_response.json()
        access_token = data["access_token"]

        print("\nVerifying access token JWT...")

        jwt = validate_eve_jwt(access_token)
        character_id = jwt["sub"].split(":")[2]
        character_name = jwt["name"]
        wallet_path = ("https://esi.evetech.net/latest/characters/{}/"
                          "wallet/".format(character_id))

        print("\nSuccess! Here is the payload received from the EVE SSO: {}"
              "\nYou can use the access_token to make an authenticated "
              "request to {}".format(data, wallet_path))
        token_data = json.dumps(data)
        with open('token.json', 'w') as token_file:
            print(token_data, file=token_file)

        #input("\nPress any key to have this program make the request for you:")

        headers = {
            "Authorization": "Bearer {}".format(access_token)
        }

        res = requests.get('https://esi.evetech.net/latest/characters/2115788560/wallet/', headers=headers)
        print("\nMade request to {} with headers: "
              "{}".format(wallet_path, res.request.headers))
        res.raise_for_status()

        data = res.json()
        print("\n{} has {} ISK".format(character_name, data))
        res = '{} has {} ISK'.format(character_name, data)
        return res