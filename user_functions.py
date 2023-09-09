from database_user import UserDB
from database_student import StudentDB
# from database_educator import EducatorDB

def import_users_from_csv(filename) -> list[tuple]:
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

# kwargs for extra user information if student or educator
def create_new_user(username: str, password: str, user_type: str, details=None) -> bool:
    if details:
        pass
    user_db = UserDB.instance()
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