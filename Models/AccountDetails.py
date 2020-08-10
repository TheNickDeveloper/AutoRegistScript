class AccountDetails:
    def __init__(self, user_id, user_name, email_address, region):
        self.__user_id = user_id
        self.__user_name = user_name
        self.__email_address = email_address
        self.__region = region
    

    @property
    def user_id(self):
        return self.__user_id
    

    @property
    def user_name(self):
        return self.__user_name


    @property
    def region(self):
        return self.__region

    
    @property
    def email_address(self):
        return self.__email_address

    # @email_address.setter
    # def email_address(self, value):
    #     self.__email_address = value
