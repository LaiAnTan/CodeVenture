from user import User, import_users_from_csv
from database_user import UserDB
import os

if __name__ == "__main__":
    db = UserDB()
    db.new_users_db()
    if db.exists() == False:
        print("where did my db go")
    else:
        print("db exists")
    users = import_users_from_csv("test_users.txt")
    for user in users:
        db.add_user(user)
    
    test = User(users[0][2], users[0][0], users[0][1])
    user_input_pw = input("Enter password: ")
    print(test.login(user_input_pw))

# fucking