import startup
from src.logger import LoggerBot
from src.message_manager import MessageManager


obrz_bot = startup.build_obrz_bot()


@obrz_bot.tb.middleware_handler(update_types=['message'])
def middleware_handler(bot_instance, package):
    if LoggerBot.is_enabled:
        LoggerBot.send_log(package)

    pikcher = obrz_bot.pikchers.get_or_create_pikcher(package)

    is_bot_initialized = obrz_bot.initialization_handler(pikcher, package)

    if is_bot_initialized and pikcher is not None:
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
    pikcher = message.pikcher

    error = None
    if command in ['/беру', '/подумаю']:
        error = obrz_bot.article_manager.take_article(pikcher, value)
    elif command == '/на_опрос':
        error = obrz_bot.article_manager.take_poll(pikcher, value)
    elif command ==  '/не_беру':
        error = obrz_bot.article_manager.give_article_back(pikcher, value)
    elif command.startswith('/add_filter '):
        pass
    elif command.startswith('/remove_filter '):
        pass
    elif command.startswith('/reset_filter'):
        pass
    else:
        pass

    if error is not None:
        MessageManager.send_message(message.chat_id, error)


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
