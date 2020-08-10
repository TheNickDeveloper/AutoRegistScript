import os
import win32com.client as win32
import Models.EmaiModel as emailModel

class OutlookHelper():
    def __init__(self, email: emailModel.Email):
        outlook = win32.Dispatch('Outlook.Application')
        self.__mail_item = outlook.CreateItem(0)
        self.__email = email

    
    def send_mail(self):
        self.__mail_item.To = self.__email.to
        self.__mail_item.Subject = self.__email.subject
        self.__mail_item.BodyFormat = 2
        self.__mail_item.HTMLBody  = self.__email.body
        self.__mail_item.Save()

    
    def __attach_files(self):
        listOfFile = os.listdir(self.__email.attachmentPath)
        for entry in listOfFile:
            fullPath = os.path.join(self.__email.attachmentPath, entry)
            self.__mail_item.Attachments.Add(fullPath)
