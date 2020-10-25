class RecordNotFoundError(Exception):
    message = 'Desired data doest not exist'

    def __init__(self, msg=message):
        self.message = msg
        super().__init__(msg)
