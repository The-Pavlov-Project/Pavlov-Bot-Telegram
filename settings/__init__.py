import json
import logging.config
import os

from .models import SettingsLoaderModel


def setup_logger():
    """logger initialization from config file"""
    try:
        with open("logger.json", 'r') as f:
            logging_configs = json.load(f)
            logging.config.dictConfig(logging_configs)
            return

    except FileNotFoundError:
        logging.basicConfig(level=logging.INFO)


class SettingModule(SettingsLoaderModel):

    CONFIGURATIONS_MODEL_FILENAME = 'secrets.json'

    token: str = os.getenv('TOKEN')
    proxy: str = ""


setting_module = SettingModule()
setting_module.load()
