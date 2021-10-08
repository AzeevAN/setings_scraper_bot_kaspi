from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
HOST_FTP = env.str("HOST_FTP")
USER_FTP = env.str("USER_FTP")
PASSWORD_FTP = env.str("PASSWORD_FTP")
PORT_FTP = env.str("PORT_FTP")
