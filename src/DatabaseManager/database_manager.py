import requests
import json

from telebot.types import InputMediaDocument


class DatabaseManager:
    def __init__(self, telebot):
        self._tb = telebot

    def create_db_message(self, user):
        with open('PlaceholderFile', 'w', encoding='utf-8') as db_file:
            db_file.write("Placeholder")
        with open('PlaceholderFile', 'rb') as db_file:
            db_message = self._tb.send_document(user.chat_id, db_file)
            db_message_id = db_message.message_id
            user.set_data('databaseMessageId', db_message_id)

    def load_db(self, chat_id, db_message_id):
        db_message = self._get_db_message(chat_id, db_message_id)
        file_path = self._tb.get_file(db_message.document.file_id).file_path
        FILE_URL = 'https://api.telegram.org/file/bot{0}/{1}'
        db_str = requests.get(FILE_URL.format(self._tb.token, file_path)).text

        db_dict = json.loads(db_str)

        return db_dict

    def save_db(self, users, db_dict):
        with open('bot_database.json', 'w', encoding='utf-8') as db_file:
            json.dump(db_dict, db_file)
        with open('bot_database.json', 'rb') as db_file:
            db_doc = InputMediaDocument(db_file)
            for user in users:
                db_message_id = user.data.get('databaseMessageId')
                if db_message_id is None:
                    continue

                self._tb.edit_message_media(
                    media=db_doc,
                    chat_id=user.chat_id,
                    message_id=db_message_id)

    def _get_db_message(self, chat_id, db_message_id):
        db_message = self._tb.edit_message_caption(
            "<i>Загрузка сообщения...</i>",
            chat_id=chat_id,
            message_id=db_message_id,
            parse_mode='HTML')

        db_message = self._tb.edit_message_caption(
            " ",
            chat_id=chat_id,
            message_id=db_message_id,)

        return db_message
