import re
from email.utils import parseaddr


class RegistrationCheck:
    def __init__(self, forename, surname,email, password, isCustomer):
        self.forename = forename
        self.surname = surname
        self.email = email
        self.password = password
        self.isCustomer = isCustomer

    def EmptyCheck(self):
        message = ""
        if (len(self.forename) == 0):
            message = "Field forename is missing. "
        elif (len(self.surname) == 0):
            message = "Field surname is missing. "
        elif (len(self.email) == 0):
            message = "Field email is missing. "
        elif (len(self.password) == 0):
            message = "Field password is missing. "
        elif (len(str(self.isCustomer)) == 0):
            message = "Field isCustomer is missing. "
        message = message if message == "" else message[:-1]
        return message;

    def EmailCheck(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (not bool(re.fullmatch(regex, self.email))):
            return "Invalid email."
        return ""

    def PasswordCheck(self):
        if (len(self.password) < 8):
            return "Invalid password."
        if (bool(re.search('[0-9]+', self.password)) == False):
            return "Invalid password."
        if (bool(re.search('[a-z]+', self.password)) == False):
            return "Invalid password."
        if (bool(re.search('[A-Z]+', self.password)) == False):
            return "Invalid password."
        return ""

    #def CustomerCheck(self):
    #    tacno = True,
    #   netacno = False
    #    if(self.isCustomer == 1):
    #       return tacno;
    #    if (self.isCustomer == 0):
    #        return netacno;



