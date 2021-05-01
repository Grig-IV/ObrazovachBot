class Message:
    def __init__(self):
        self.text = str()
        self.parse_mode = 'HTML'

    def get_kwargs(self):
        raise NotImplementedError("Subclass must implement get_kwargs method")