from database.database_user import UserDB
from database.database_student import StudentDB
# from database_educator import EducatorDB

def import_data_from_csv(filename) -> list[tuple]:
    """
    Reads from a csv file containing user data
    and converts it into a list of tuples for database insertion
    """
    l = list()
    with open(filename, "r") as f:
        for line in f:
            line = line.rstrip('\n')
            if line == "" or line[0] == "#":
                continue
            values = line.split(",")
            l.append((values))
    return l

def create_new_user(username: str, password: str, user_type: str, details=None) -> bool:
    if details:
        pass
    user_db = UserDB()
    try:
        user_db.add_user((username, password, user_type))
    except user_db.UserExistsException:
        return False
    match user_type:
        case "student":
            student_db = StudentDB()
            if details:
                student_db.add_student(details)
        case "educator":
            pass
            # educator_db = EducatorDB()
            # if details:
            #     educator_db.add_educator(details)
        case _: # should never happen
            pass
    return True

def populate_databases():
    """
    Populate databases with test data
    """

    # change test data filenames here
    test_users_filename = "test_data/test_users.txt"
    test_students_filename = "test_data/test_students.txt"
    test_educators_filename = "test_data/test_educators.txt"
    test_admins_filename = "test_data/test_admins.txt"

    # init databases
    db = UserDB()
    sdb = StudentDB()
    # edb = EducatorDB()
    # adb = AdminDB()

    database_list = [db, sdb] # add more as time goes on


    users = import_data_from_csv(test_users_filename)
    students = import_data_from_csv(test_students_filename)

    entries_list = [users, students] # add more as time goes on (corespond to database_list)

    # init .db files
    for database in database_list:
        if database.db_exists() == False:
            database.new_db()

    # populate
    for i in range(2):
        database = database_list[i]
        for entry in entries_list[i]:
            try:
                database.add_entry(entry)
            except database.DuplicateEntryException:
                continue

    print("Populated databases")