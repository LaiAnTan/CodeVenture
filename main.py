from user import User, import_users_from_csv
from database_user import UserDB
import os

if __name__ == "__main__":
    UserDB.make_singleton()
    users = import_users_from_csv("test_users.txt")
    if os.path.isfile("users.db") == False:
        UserDB.new_users_db()
    for user in users:
        UserDB.add_user(user)
    print(UserDB.fetch_attr("password", "tlai-an"))
    # this is dangerous
    os.remove("users.db")