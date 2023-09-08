import sqlite3 as sqlite3
import os
class UserDB:
    
    def __init__(self):
        # open connection & init cursor
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "users.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        print("Connected")

    def exists(self):
        with self.conn:
            self.cursor.execute("""SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='users'""")
            if self.cursor.fetchone() == []:
                return False
            else:
                return True

    def new_users_db(self):
        # ONLY RUN THIS FUNCTION IF YOU WANT A NEW USERS DATABASE TO BE CREATED
        # specify the fields below
        with self.conn:
            if self.exists() == False:
                self.cursor.execute("""
                                CREATE TABLE users(
                                    username text,
                                    password text,
                                    name text
                                )
                                """)
                self.conn.commit()

    def add_user(self, user_data: tuple):
        # used placeholder (?) instead of named fields for easy addition of new fields in the future
        with self.conn:
            self.cursor.execute("""INSERT INTO users VALUES (?, ?, ?)""", user_data)
            self.conn.commit()
    
    def remove_user(self, username):
        with self.conn:
            self.cursor.execute("""DELETE FROM users WHERE username=:username""", {"username": username})
            self.conn.commit()
    
    def fetch_attr(self, field, username):
        # fetches the required attribute with the username that matches it
        with self.conn:
            return self.cursor.execute(f"SELECT {field} from users WHERE username=:username", {"username": username}).fetchone()

if __name__ == "__main__":
    pass