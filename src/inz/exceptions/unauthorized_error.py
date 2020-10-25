class UnauthorizedError(Exception):
    message = 'Cannot access desired data'

    def __init__(self, msg=message):
        self.message = msg
        super().__init__(msg)
