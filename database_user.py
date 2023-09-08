import sqlite3 as sqlite3
import os
class UserDB:

    """
    Singleton class that handles users database operations
    """
    db_name = "users"
    
    # database path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, f"{db_name}.db")

    _instance = None

    db_fields = """
                username text, 
                password text, 
                user_type text
                """
    
    # placeholder for field
    db_placeholders = "(" + "".join(["?, " for i in range(len(db_fields.split(",")) - 1)]) + "?" + ")"
    
    # connection and cursor
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    class UserExistsException(Exception):
        """Called when trying to add user that already exists in the database"""
        
        def __init__(self, msg="User already exists in the database"):
            super().__init__(msg)
    
    class UserNotFoundException(Exception):
        """Called when trying to delete user that does not exist in the database"""
        def __init__(self, msg="User not found in the database"):
            super().__init__(msg)

    @classmethod
    def instance(cls):
        """Creates a new instance if it doesnt already exist"""
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    @classmethod
    def db_exists(cls):
        cls.cursor.execute(f"""SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='{cls.db_name}'""")
        return cls.cursor.fetchone() != None

    @classmethod
    def new_users_db(cls):
        # ONLY RUN THIS FUNCTION IF YOU WANT A NEW USERS DATABASE TO BE CREATED
        if cls.db_exists() == False:
            cls.cursor.execute(f"CREATE TABLE {cls.db_name}({cls.db_fields})")
            cls.conn.commit()

    @classmethod
    def add_user(cls, user_data: tuple):
        # used placeholder (?) instead of named fields for easy addition of new fields in the future
        if cls.fetch_attr("username", user_data[0]) != None:
            raise cls.UserExistsException
        cls.cursor.execute(f"INSERT INTO {cls.db_name} VALUES {cls.db_placeholders}", user_data)
        cls.conn.commit()

    @classmethod
    def remove_user(cls, username):
        if cls.fetch_attr("username", username) == None:
            raise cls.UserNotFoundException
        cls.cursor.execute(f"DELETE FROM {cls.db_name} WHERE username=:username", {"username": username})
        cls.conn.commit()

    @classmethod
    def fetch_attr(cls, field, username):
        # fetches the required attribute with the username that matches it
        # returns None if user not found
        return cls.cursor.execute(f"SELECT {field} from {cls.db_name} WHERE username=:username", {"username": username}).fetchone()

if __name__ == "__main__":
    pass