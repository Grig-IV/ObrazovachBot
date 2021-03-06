import startup
from src.Services.telebot_provider import TelebotProvider


obrz_bot = startup.build_obrz_bot()
telebot = TelebotProvider.get_telebot()


@telebot.message_handler(content_types=['text'])
def commands_handler(message):
    message = obrz_bot.middleware_handler(message)

    if not message.access_token:
        return

    command, value = obrz_bot.parse_command(message.text)
    pikcher = message.pikcher

    if command == '/start':
        obrz_bot.db_manager.create_db_message(pikcher)
        obrz_bot.save_db()
        obrz_bot.article_module.create_article_message(pikcher)
    elif command in ['/беру', '/подумаю']:
        obrz_bot.article_module.take_article(pikcher, value)
    elif command == '/на_опрос':
        obrz_bot.article_module.take_poll(value)
    elif command == '/не_беру':
        obrz_bot.article_module.give_article_back(value)
    elif command.startswith('/add_filter '):
        pass
    elif command.startswith('/remove_filter '):
        pass
    elif command.startswith('/reset_filter'):
        pass
    else:
        pass


@telebot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    call = obrz_bot.middleware_handler(call)

    if not call.access_token:
        return

    action, value, _ = call.data.split()
    pikcher = call.pikcher

    if action == 'switch_page':
        obrz_bot.article_module.switch_page(pikcher, int(value))
    elif action == 'switch_article_type':
        obrz_bot.article_module.switch_article_type(pikcher, value)
    elif action == 'refresh':
        obrz_bot.article_module.update_article_db()


@telebot.message_handler(content_types=['document'])
def doc_for_init_handler(db_message):
    db_message = obrz_bot.middleware_handler(db_message)

    pass


telebot.polling(none_stop=True)
