from database.database_base import DBBase
import csv
from enum import Enum

class ActivityDB(DBBase):
    """
    sex man
    """

    class field(Enum):
        id = 0
        type = 1
        title = 2
        difficulty = 3
        tags = 4
        description = 5

    @classmethod
    def __new__(cls, placeholder):
        return super().__new__(
            "activities",
            """
            id text,
            type integer,
            title text,
            difficulty integer,
            tags text,
            description text
            """
        )

    @classmethod
    def get_list_of_id(cls, type):
        if type == 0:
            type = ""
        else:
            type = f"WHERE type = {type}"

        raw_data = cls.cursor.execute(f"SELECT {cls.db_idfield} from {cls.db_name} {type}").fetchall()
        ## stupid shit returning in tuple
        ret_value = [id[0] for id in raw_data]
        return ret_value


def import_data_from_csv_activity(path) -> list[tuple]:
    """
    Reads from a csv file containing user data
    and converts it into a list of tuples for database insertion
    
    delimiter is | for activity
    """
    with open(path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        ret = [row for row in csv_reader]
    return ret

# def populate_activityDatabase(path: str):
#     database = ActivityDB()
#     data_full = import_data_from_csv_activity(path)

#     database.new_db()

#     for data in data_full:
#         print("data")
#         print(data)
#         print()
#         try:
#             database.add_entry(data)
#         except database.DuplicateEntryException:
#             continue

if __name__ == "__main__":
    pass
    # populate_activityDatabase()
    # database = ActivityDB()
    # test = database.retrieve_all_attr("MD0000")
    # print(test[ActivityDB.field.id.value])
    
    # for x in range(4):
    #     result = database.get_list_of_id(x)
    #     print(result)