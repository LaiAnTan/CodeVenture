import sqlite3
from abc import ABC, abstractmethod
from database_user import UserDB
# should i use abstract base class hmmm

class User(ABC):

    def __init__(self, username):
        """
        Initializes the User abstract class.
        Note only the username is saved here,
        and will be used to query for other values in the database.
        """
        self.username = username
        self.login_status = False
    
    """
    Getters
    """
    def get_username(self) -> str:
        return self.username
    
    """
    Setters
    """
    def set_username(self, username: str) -> None:
        self.username = username
    
    """
    Methods
    """
    def login(self, pw_input) -> bool:
        """
        Tries to match pw_input with password from db
        """
        # accessing db (UserDB.make_singleton() must be called before this)
        db = UserDB.instance()
        user_pw = db.fetch_attr("password", self.get_username())
        if user_pw == None: # user not in database
            return False
        elif user_pw[0] == pw_input: # login success
            self.login_status = True
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