import os
import os.path
import json    
            

def setup_settings():
    print('Trying to get your settings!') 
    if os.stat('settings.json').st_size == 0:
        print('Need to setup your settings!')
        client_id = input("Your cliend ID: ")
        client_secret = input('Your client secret: ')
        callback_url = input('Your callback url: ')
        data = {
            'settings' : [
                {
                    "client_id" : client_id,
                    "client_secret" : client_secret,
                    "callback_url" : callback_url,
                }
            ]
        }
        settings = json.dumps(data)
        with open('settings.json', 'w') as settings_file:
            print(settings, file=settings_file)
        print("Everything is ok!")
    else:
        with open('settings.json', 'r') as settings_file:
            data = json.load(settings_file)
            print('Your settings: ', data)

def change_settings():
    print('Changing your settings!')
    print('Need to setup your settings!')
    client_id = input("Your cliend ID: ")
    client_secret = input('Your client secret: ')
    callback_url = input('Your callback url: ')
    data = {
            'settings' : [
                {
                    "client_id" : client_id,
                    "client_secret" : client_secret,
                    "callback_url" : callback_url
            }
        ]
    }
    settings = json.dumps(data)
    with open('settings.json', 'w') as settings_file:
        print(settings, file=settings_file)
    print("Everything is ok!")

def settings_first_run():
    try: 
        os.stat('settings.json').st_size == 0
        setup_settings()
    except FileNotFoundError:
        print('Settings file does not exist! Creating settigns file!')
        with open('settings.json', 'w') as settings_file:
            print('Settings file is created!')
            setup_settings()

def main():
    try: 
        os.stat('settings.json').st_size == 0
        setup_settings()
    except FileNotFoundError:
        print('Settings file does not exist! Creating settigns file!')
        with open('settings.json', 'w') as settings_file:
            print('Settings file is created!')
            setup_settings()


if __name__ == "__main__":
    main()