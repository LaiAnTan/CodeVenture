import sqlite3 as sqlite3

class UserDB:
    
    instance = None
    
    def __init__(self):
        # open connection & init cursor
        UserDB.conn = sqlite3.connect("users.db")
        UserDB.cursor = UserDB.conn.cursor()

    def __del__(self):
        # close connection
        UserDB.conn.close()

    @classmethod
    def new_users_db(cls):
        # ONLY RUN THIS FUNCTION IF YOU WANT A NEW USERS DATABASE TO BE CREATED
        # specify the fields below
        UserDB.cursor.execute("""
                        CREATE TABLE users(
                            username text,
                            password text,
                            name text
                        )
                        """)
        UserDB.conn.commit()

    @classmethod
    def add_user(cls, user_data: tuple):
        # used placeholder (?) instead of named fields for easy addition of new fields in the future
        UserDB.cursor.execute("""INSERT INTO users VALUES (?, ?, ?)""", user_data)
        UserDB.conn.commit()
    
    @classmethod
    def fetch_attr(cls, field, username):
        # fetches the required attribute with the username that matches it
        UserDB.cursor.execute(f"SELECT {field} from users WHERE username=:username", {"username": username})
        return UserDB.cursor.fetchone()
    
    @classmethod
    def make_singleton(cls):
        cls.instance = UserDB()

if __name__ == "__main__":
    pass