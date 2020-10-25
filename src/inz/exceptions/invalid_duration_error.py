class InvalidDurationError(Exception):
    message = 'Start date must precede end date'

    def __init__(self, msg=message):
        self.message = msg
        super().__init__(msg)
