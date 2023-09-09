from user.user_base import User
from user_functions import import_users_from_csv, create_new_user
from database.database_base import DBBase
from database.database_user import UserDB
import os
if __name__ == "__main__":
    db = UserDB()
    db.new_db()
    if db.db_exists() == False:
        print("where did my db go")
    else:
        print("db exists")
    users = import_users_from_csv("test_users.txt")
    for user in users:
        try:
            db.add_entry(user)
        except db.DuplicateEntryException:
            continue
    
    test = User(users[0][0])
    user_input_pw = input("Enter password: ")
    print(test.login(user_input_pw))

    print(db.update_attr("username", "john", "heh"))
