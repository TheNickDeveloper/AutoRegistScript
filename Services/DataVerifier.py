from Services.ExceptionHelper import BlankDataException

class DataVerifier:
    def is_null(self, val, col_name):
        v = str(val).strip()
        if v == 'nan':
            raise BlankDataException(f"{col_name} cannot be blank.")
        if not len(v):
            raise BlankDataException(f"{col_name} cannot be blank.")

        return val



