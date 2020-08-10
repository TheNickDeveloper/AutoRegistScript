import os, sys
sys.path.append(os.getcwd())

from Models.AccountDetails import AccountDetails

class Email:
    def __init__(self, account_details:AccountDetails):
        self.__account_details = account_details


    @property
    def to(self):
        return self.__account_details.email_address


    @property
    def subject(self):
        return "Enroll account completed"

    
    @property
    def body(self):
        return f'''
                hi {self.__account_details.user_name}<br/>
                <br/>
                Please note your account enroll has completed. <br/>
                Account: {self.__account_details.user_id}<br/>
                Password: 1111<br/>
                <br/>
                BR<br/>
                Nick Tsai
            '''