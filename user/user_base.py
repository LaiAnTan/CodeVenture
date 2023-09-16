import sqlite3
from abc import ABC, abstractmethod
from database.database_user import UserDB
from settings import Settings

class User(ABC):

    def __init__(self, username):
        """
        Initializes the User abstract class.
        Note only the username is saved here,
        and will be used to query for other values in the database.
        """
        self.username = username
        self.login_status = False
        self.user_type = None
    
    """
    Getters
    """
    def getUsername(self) -> str:
        return self.username
    
    def getUserType(self):
        return self.user_type

    """
    Setters
    """

    def setUsername(self, username: str) -> None:
        self.username = username
    
    """
    Methods
    """
    def login(self, pw_input) -> bool:
        """
        Tries to match pw_input with password from db
        """
        db = UserDB()
        user_pw = db.fetch_attr("password", self.getUsername())
        if user_pw == None: # user not in database
            return False
        elif user_pw == pw_input: # login success
            self.login_status = True
            self.user_type = db.fetch_attr("user_type", self.getUsername())
            print(self.user_type)
            return True
        else: # login failed
            return False
    
    def logout(self) -> bool:
        self.login_status = False
    
    # @abstractmethod
    # def export_user_data():
    #     pass

if __name__ == "__main__":
    from user_functions import import_users_from_csv

    print(import_users_from_csv("test_users.txt"))