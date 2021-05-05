class Message:
    def __init__(self, text):
        self.text = text
        self.parse_mode = None
        self.disable_web_page_preview = True
        self.reply_markup = None

    def get_kwargs(self):
        kwargs = dict()

        kwargs['text'] = self.text
        kwargs['disable_web_page_preview'] = disable_web_page_preview

        if parse_mode is not None:
            kwargs['parse_mode'] = self.parse_mode
        if reply_markup is not None:
            kwargs['reply_markup'] = self.reply_markup

        return kwargs
