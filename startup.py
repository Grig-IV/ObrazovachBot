import json

from telebot import TeleBot
from telebot import apihelper

from src.logger import LoggerBot
from src.obrazovach_bot import ObrazovachBot


apihelper.ENABLE_MIDDLEWARE = True


def build_obrz_bot():
    launch_settings_file = open("LaunchSettings.json", 'r')
    launch_settings = json.load(launch_settings_file)
    launch_settings_file.close()

    bot_config_file = open("ObrazovachBotConfig.json", 'r')
    bot_config = json.load(bot_config_file)
    bot_config_file.close()
    
    if launch_settings['project_state'] == "Development":
        token = launch_settings['test_bot_token']
    elif launch_settings['project_state'] == "Production":
        token = launch_settings['bot_token']

        logger_token = launch_settings['test_bot_token']
        LoggerBot.enable(logger_token)

    telebot = TeleBot(token)
    obrz_bot = ObrazovachBot(telebot, **bot_config)

    return obrz_bot
