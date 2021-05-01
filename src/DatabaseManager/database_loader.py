import json


class DB_Loader:
    _tb = None

    def init(telebot):
        DB_Loader._tb = telebot

    def load_from_message(message_id):
        file_path = DB_Loader.tb.get_file(message_id.document.file_id).file_path
        url = 'https://api.telegram.org/file/bot{0}/{1}'
        db_str = requests.get(url.format(tb.token, file_path)).text

        db_dict = json.loads(db_str)

        return db_dict
