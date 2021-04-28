import startup
from src.logger import LoggerBot


obrz_bot = startup.build_obrz_bot()


@obrz_bot.tb.middleware_handler(update_types=['message'])
def middleware_handler(bot_instance, package):
    if LoggerBot.is_enabled:
        LoggerBot.send_log(package)

    pikcher = obrz_bot.pikchers.get_or_create_pikcher(package)

    obrz_bot.initializer.initialization_handler(pikcher, package)

    if obrz_bot.is_initialized and pikcher:
        package.access_token = True
        package.pikcher = pikcher
    else:
        package.access_token = False


@obrz_bot.tb.message_handler(content_types=['text'])
def commands_handler(message):
    if not message.access_token:
        return

    parser = lambda t: (t.split()[0].strip(), t.split()[1:].strip())
    command, value = parser(message.text)

    if command in ['/беру', '/подумаю']:
        pass
    elif command == '/на_опрос':
        pass
    elif command ==  '/не_беру':
        pass
    elif command.startswith('/add_filter '):
        pass
    elif command.startswith('/remove_filter '):
        pass
    elif command.startswith('/reset_filter'):
        pass
    else:
        pass

@obrz_bot.tb.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if not call.access_token:
        return
    
    action, value, _ = call.data.split()

    if action == 'switch_page':
        pass
    elif action == 'switch_artcls_type':
        pass
    elif action == 'refresh':
        pass

@obrz_bot.tb.message_handler(content_types=['document'])
def doc_for_init_handler(db_message):
    print(db_message.access_token)
    
    pass


obrz_bot.tb.polling(none_stop=True)
