import sqlite3 as sqlite3
import os

class Database:

    """
    Singleton class that handles users database operations
    """
    
    # database filename
    name = None
    
    # database path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, name)
    
    # instance
    _instance = None
    
    # specify the fields below
    db_fields = """
                username text, 
                password text, 
                name text
                """
    
    # placeholder for field
    db_placeholders = "(" + "".join(["?, " for i in range(len(db_fields.split(",")) - 1)]) + "?" + ")"
    
    # connection and cursor
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    @classmethod
    def instance(cls, name):
        """Creates a new instance if it doesnt already exist"""
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.name = name
        return cls._instance

    @classmethod
    def db_exists(cls):
        cls.cursor.execute(f"""SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='{cls.name}'""")
        return cls.cursor.fetchone() != None

    @classmethod
    def new_db(cls):
        # ONLY RUN THIS FUNCTION IF YOU WANT A NEW USERS DATABASE TO BE CREATED
        if cls.db_exists() == False:
            cls.cursor.execute(f"CREATE TABLE {cls.name}({cls.db_fields})")
            cls.conn.commit()

if __name__ == "__main__":
    pass