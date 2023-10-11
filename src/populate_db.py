from .backend.database.database_user import UserDB
from .backend.database.database_student import StudentDB
from .backend.database.database_activity import ActivityDB
import csv
# from database_educator import EducatorDB


def import_data_from_csv(filename) -> list[tuple]:
    """
    Reads from a csv file containing user data
    and converts it into a list of tuples for database insertion
    """
    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        ret = [row for row in csv_reader]
    return ret


def populate_databases():
    """
    Populate databases with test data
    """

    # change test data filenames here
    test_users_filename = "test_data/test_users.txt"
    test_students_filename = "test_data/test_students.txt"
    test_educators_filename = "test_data/test_educators.txt"
    test_admins_filename = "test_data/test_admins.txt"
    test_activities_filename = "test_data/test_activities.txt"

    # init databases
    db = UserDB()
    sdb = StudentDB()
    adb = ActivityDB()
    # edb = EducatorDB()
    # adb = AdminDB()

    # add more as time goes on
    database_list = [db, sdb, adb]

    users = import_data_from_csv(test_users_filename)
    students = import_data_from_csv(test_students_filename)
    activity = import_data_from_csv(test_activities_filename)

    # add more as time goes on (corespond to database_list)
    entries_list = [users, students, activity]

    # init .db files
    for database in database_list:
        if database.db_exists() == False:
            database.new_db()

    # populate
    for i, database in enumerate(database_list):
        for entry in entries_list[i]:
            try:
                database.add_entry(entry)
            except database.DuplicateEntryException:
                continue

    print("Populated databases")
