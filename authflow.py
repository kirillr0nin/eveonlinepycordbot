import urllib
import requests
import json 

def print_auth_url():
    with open('settings.json', 'r') as f:
            d = json.loads(f.read())

    client_id = d['settings'][0]["client_id"]
    callback_url = d['settings'][0]["callback_url"]
    base_auth_url = "https://login.eveonline.com/v2/oauth/authorize/"
    params = {
        "response_type": "code",
        "redirect_uri": callback_url,
        "client_id": client_id,
        "scope": 'publicData ' + 'esi-skills.read_skills.v1 ' + 'esi-wallet.read_character_wallet.v1 ' + 'esi-characters.read_standings.v1 ' + 'esi-markets.read_character_orders.v1',
        "state": "12sda42r"
    }
    string_params = urllib.parse.urlencode(params)
    full_auth_url = "{}?{}".format(base_auth_url, string_params)
    print("\nOpen the following link in your browser:\n\n {} \n\n Once you "
          "have logged in as a character you will get redirected to "
          "https://localhost/callback/.".format(full_auth_url))
    return(full_auth_url)

def main():
    print('Right? Wrong!')

if __name__ == "__main__":
    main()