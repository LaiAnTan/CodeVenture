import sqlite3
from abc import ABC, abstractmethod
# should i use abstract base class hmmm

class User(ABC):

    def __init__(self, name, username, password):
        """
        Initializes the User abstract class.
        Note only the username is saved here,
        and will be used to query for other values in the database.
        """
        self.username = username
        self.login = False
    
    """
    Getters
    """
    def get_username() -> str:
        return self.username
    
    """
    Setters
    """
    def set_username(username: str) -> None:
        self.username = username
    
    """
    Methods
    """
    def login(pw_input) -> bool:
        """
        Tries to match pw_input with password from db
        """
        # accessing db
        user_conn = sqlite3.connect('users.db')
        user_cursor = user_conn.cursor()
        user_cursor.execute("SELECT password from users WHERE username=:username", {"username": self.username})
        user_pw = user_cursor.fetchone()
        
        if user_pw == None: # user not in database
            return False
        elif user_pw == pw_input: # login success
            self.login = True
            return True
        else: # login failed
            return False
    
    def logout() -> bool:
        self.login = False
    
    @abstractmethod
    def export_user_data():
        pass

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