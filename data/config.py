from environs import Env
import json
import os
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
HOST_FTP = env.str("HOST_FTP")
USER_FTP = env.str("USER_FTP")
PASSWORD_FTP = env.str("PASSWORD_FTP")
PORT_FTP = env.str("PORT_FTP")


def load_file_json():
    with open(f'{os.getcwd()}/brands.json', 'r', encoding='utf-8') as file:
        new_value = json.load(file)

    return new_value
