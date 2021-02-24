import json


def get_config_from_file():
    global linux
    global windows
    global lin_username
    global lin_password
    global roleuser
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        linux = config_data['servers'][0]['ip'][0]
        print(f'{config_data["servers"][0]["name"]}: {linux}')
        windows = config_data['servers'][1]['ips']
        print(f'{config_data["servers"][1]["name"]}: {windows}')
        lin_username = config_data['servers'][0]['credentials'][0]['username']
        print(lin_username)
        lin_password = config_data['servers'][0]['credentials'][0]['password']
        print(lin_password)
        win_username = config_data['servers'][1]['credentials'][0]['username']
        print(win_username)
        win_password = config_data['servers'][1]['credentials'][0]['password']
        print(win_password)
    return linux, windows, lin_username, lin_password


get_config_from_file()