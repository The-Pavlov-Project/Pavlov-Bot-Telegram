import json
from .modules.paginator import Paginator
from .modules.configs import Configs

FILE_CONFIG_DIR = 'commands/miscellaneous/post/configs.json'
with open(FILE_CONFIG_DIR, 'r') as f:
    CONFIG_DATA = json.loads(f.read())

# H, P, T
ADMINS = ['338674622', '36974410']

