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
        db = UserDB()
        user_pw = db.fetch_attr("password", self.get_username())
        if user_pw == None: # user not in database
            return False
        elif user_pw[0] == pw_input: # login success
            self.login_status = True
            return True
        else: # login failed
            return False
    
    def logout() -> bool:
        self.login_status = False
    
    # @abstractmethod
    # def export_user_data():
    #     pass

def import_users_from_csv(filename) -> list[tuple]:
    """
    Reads from a csv file containing user data
    and converts it into a list of tuples for database insertion
    """
    l = list()
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip('\n')
            if line == "" or line[0] == "#":
                continue
            values = line.split(",")
            l.append((values))
    return l

if __name__ == "__main__":
    print(import_users_from_csv("test_users.txt"))