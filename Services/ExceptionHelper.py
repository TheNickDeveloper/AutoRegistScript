class BlankDataException(Exception):
    def __init__(self, col_name):
        self.message = f'{col_name} cannot be balnk.'
        super().__init__(self.message)
    def __str__(self):
            return repr(self.message)