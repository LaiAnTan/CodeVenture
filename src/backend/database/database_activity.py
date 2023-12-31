from enum import Enum
from .database_base import DBBase


class ActivityDB(DBBase):
    """
    Singleton class that handles activity database operations
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
        # changes type from tuple to list
        ret_value = [id[0] for id in raw_data]
        return ret_value

    @classmethod
    def getIDandType(cls):
        raw_data = cls.cursor.execute(f"SELECT id, type from {cls.db_name}").fetchall()
        return raw_data

    @classmethod
    def getIDTypeTitle(cls):
        raw_data = cls.cursor.execute(f"SELECT id, type, title from {cls.db_name}").fetchall()
        return raw_data

    @classmethod
    def checkIDExists(cls, id):
        return cls.fetch_attr(cls.db_idfield, id) != None
    
    @classmethod
    def getAllowedTags(cls):
        from config import TAG_DIR
        with open(TAG_DIR, 'r') as tag_fd:
            tag_labels = [x.strip('\n') for x in tag_fd.readlines()]
        return tag_labels
