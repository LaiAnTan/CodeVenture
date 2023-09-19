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
    def getListID(cls, type):
        if type == 0:
            type = ""
        else:
            type = f"WHERE type = {type}"

        raw_data = cls.cursor.execute(f"SELECT {cls.db_idfield} from {cls.db_name} {type}").fetchall()
        ## stupid shit returning in tuple
        ret_value = [id[0] for id in raw_data]
        return ret_value

    @classmethod
    def getIDandType(cls):
        raw_data = cls.cursor.execute(f"SELECT id, type from {cls.db_name}").fetchall()
        return raw_data