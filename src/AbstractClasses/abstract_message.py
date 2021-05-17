class Message:
    def __init__(self, text, parse_mode=None,
                 disable_web_page_preview=True,
                 reply_markup=None):
        self.text = text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.reply_markup = reply_markup

    def get_kwargs(self):
        kwargs = dict()

        kwargs['text'] = self.text
        kwargs['disable_web_page_preview'] = self.disable_web_page_preview

        if self.parse_mode is not None:
            kwargs['parse_mode'] = self.parse_mode
        if self.reply_markup is not None:
            kwargs['reply_markup'] = self.reply_markup

        return kwargs
