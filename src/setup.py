import os
import csv
from argon2 import PasswordHasher

from .backend.database.database_user import UserDB
from .backend.database.database_student import StudentDB
from .backend.database.database_activity import ActivityDB
from .backend.activity.ac_database.db_ac_completed import ActivityDictionary
from config import ROOT_DIR, DATABASE_DIR


def import_data_from_csv(filename: str) -> list[tuple]:
    """
    Reads from a csv file containing user data
    and converts it into a list of tuples for database insertion
    """
    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=":")
        ret = [row for row in csv_reader]
    return ret


def populate_databases():
    """
    Populate databases with test data
    """

    # change test data filenames here
    test_users_filename = f"{ROOT_DIR}/test_data/test_users.txt"
    test_students_filename = f"{ROOT_DIR}/test_data/test_students.txt"
    test_activities_filename = f"{ROOT_DIR}/test_data/test_activities.txt"

    # init databases
    db = UserDB()
    sdb = StudentDB()
    adb = ActivityDB()

    # add more as time goes on
    database_list = [db, sdb, adb]

    users = import_data_from_csv(test_users_filename)
    students = import_data_from_csv(test_students_filename)
    activity = import_data_from_csv(test_activities_filename)

    # hash the passwords
    ph = PasswordHasher()
    for i, user in enumerate(users):
        users[i][1] = ph.hash(user[1])

    # add more as time goes on (corespond to database_list)
    entries_list = [users, students, activity]

    # init .db files
    for database in database_list:
        if database.db_exists() is False:
            database.new_db()

    # populate
    for i, database in enumerate(database_list):
        for entry in entries_list[i]:
            try:
                database.add_entry(entry)
            except database.DuplicateEntryException:
                continue

    ActivityDictionary()
    print("Populated databases")


def reset_databases() -> None:
    """
    Resets the databases by deleting .db files
    """
    files = os.listdir(DATABASE_DIR)

    for file in files:
        if file.split(".")[1] == 'db':
            file_path = os.path.join(DATABASE_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    print("Resetted databases")
