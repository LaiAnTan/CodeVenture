import sqlite3 as sqlite3
import os

class StudentDB:

    """
    Singleton class that handles student database operations
    """
    
    db_name = "students"
    
    # database path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, f"{db_name}.db")

    _instance = None

    """
    notes:
    - subscription is boolean (0, 1)
    - quiz results and challenge results are strings
    that are converted from a list of objects
    between objects they are seperated by ;
    internally they are seperated by ,
    """
    db_fields = """
                username text,
                subscription integer,
                date_of_birth text,
                quiz_results text,
                challenge_results texxt
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
    def new_student_db(cls):
        # ONLY RUN THIS FUNCTION IF YOU WANT A NEW USERS DATABASE TO BE CREATED
        if cls.db_exists() == False:
            cls.cursor.execute(f"CREATE TABLE {cls.db_name}({cls.db_fields})")
            cls.conn.commit()

    @classmethod
    def add_student(cls, student_details: tuple):
        # used placeholder (?) instead of named fields for easy addition of new fields in the future
        if cls.fetch_attr("username", student_details[0]) != None:
            raise cls.UserExistsException
        cls.cursor.execute(f"INSERT INTO {cls.db_name} VALUES {cls.db_placeholders}", student_details)
        cls.conn.commit()

    @classmethod
    def remove_student(cls, username):
        if cls.fetch_attr("username", username[0]) == None:
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