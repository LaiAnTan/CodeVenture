import sqlite3 as sql
import os

from config import ACTIVITY_DIR
from src.backend.activity.ac_classes.ac_activity import Activity


class CompletedDB():

    """
    Database for storing completions of students.
    """

    def __init__(self, ac_id, ac_type, fields: str) -> None:
        """
        Initialises the class.
        """

        self.db_name = "completed"

        # what the hell is this
        # self.root = os.path.split(os.path.split(os.path.split(os.path.split(os.path.dirname(__file__))[0])[0])[0])[0]

        self.modulePath = f"{ACTIVITY_DIR}/{ac_type.name}/{ac_id}"

        self.db_path = os.path.join(self.modulePath, f"{self.db_name}.db")
        self.db_fields = fields
        self.db_idfield = fields.split(",")[0].split()[0].strip()

        self.db_placeholder = f"({','.join(['?' for _ in self.db_fields.split(',')])})"

        self.connect = sql.connect(self.db_path)
        self.cursor = self.connect.cursor()
        self.new_db()

    def db_exist(self):
        """
        checks if the database with name db_name currently exists
        """
        self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name=(?)", (self.db_name,))
        return self.cursor.fetchone() is not None

    def new_db(self):
        """
        creates a new database with:
        - name specified in db_name
        - fields specified in db_fields
        (only works if the database doesnt currently exist)
        """
        if self.db_exist() is False:
            self.cursor.execute(f"CREATE TABLE {self.db_name}({self.db_fields})")
            self.connect.commit()

    def getStudentEntry(self, student_id):
        """
        Retrieves the student entry from the database.
        """
        value = self.cursor.execute(f"SELECT * from {self.db_name} WHERE {self.db_idfield}=(?)",(student_id,)).fetchone()
        return value

    def StudentEntryExist(self, student_id):
        """
        Check if the student entry already exists in the database.
        """
        return self.getStudentEntry(student_id) is not None

    def addStudentEntry(self, values: tuple[str]):
        """
        Adds an entry into the database.
        """
        if self.StudentEntryExist(values[0]):
            return
        self.cursor.execute(f"INSERT INTO {self.db_name} VALUES {self.db_placeholder}", values)
        self.connect.commit()


class ChallengeCompleted_DB(CompletedDB):
    def __init__(self, ac_id) -> None:
        super().__init__(
            ac_id,
            Activity.AType.Challenge,
            """
            id text,
            completion real,
            code text
            """
        )

    def getStudentCode(self, std_id) -> None:
        if not self.StudentEntryExist(std_id):
            return None
        data = self.cursor.execute(f"SELECT code from {self.db_name} WHERE {self.db_idfield}=(?)", (std_id,)).fetchone()
        return data[0]

    def updateStudentCode(self, std_id, completion, new_answer) -> None:
        if not self.StudentEntryExist(std_id):
            return self.addStudentEntry((std_id, completion, new_answer))
        self.cursor.execute(f"UPDATE {self.db_name} SET code=(?), completion=(?) WHERE {self.db_idfield}=(?)", (new_answer, completion, std_id))
        self.connect.commit()

class ModuleCompleted_DB(CompletedDB):
    def __init__(self, ac_id) -> None:
        super().__init__(
            ac_id,
            Activity.AType.Module,
            """
            id text
            """
        )


class QuizCompleted_DB(CompletedDB):
    def __init__(self, ac_id) -> None:
        super().__init__(
            ac_id,
            Activity.AType.Quiz,
            """
            id text,
            answer text
            """
        )

    def getStudentAnswer(self, std_id) -> None:
        if self.getStudentEntry(std_id) == None:
            return None
        data = self.cursor.execute(f"SELECT answer from {self.db_name} WHERE {self.db_idfield}=(?)", (std_id,)).fetchone()
        return data[0]

    def updateStudentAnswer(self, std_id, new_answer) -> None:
        if self.getStudentEntry(std_id) == None:
            return self.addStudentEntry((std_id, new_answer))
        self.cursor.execute(f"UPDATE {self.db_name} SET answer=(?) WHERE {self.db_idfield}=(?)", (new_answer, std_id))
        self.connect.commit()


class ActivityDictionary():
    _instance = None
    dictionary = {}

    @classmethod
    def __new__(cls, placeholder):
        if cls._instance:
            return cls._instance
        cls._instance = super(ActivityDictionary, cls).__new__(cls)
        cls.initialize_dict()
        return cls._instance

    @classmethod
    def databaseDispatcher(cls, activity: str, type: int):
        match type:
            case Activity.AType.Module.value:
                return ModuleCompleted_DB(activity)
            case Activity.AType.Quiz.value:
                return QuizCompleted_DB(activity)
            case Activity.AType.Challenge.value:
                return ChallengeCompleted_DB(activity)

    @classmethod
    def initialize_dict(cls):
        from src.backend.database.database_activity import ActivityDB

        list_of_id = ActivityDB().getIDandType()
        for id in list_of_id:
            cls.dictionary[id[0]] = cls.databaseDispatcher(id[0], id[1])

    @classmethod
    def getDatabase(cls, id) -> ModuleCompleted_DB | ChallengeCompleted_DB | QuizCompleted_DB:
        from src.backend.database.database_activity import ActivityDB

        if ActivityDB().checkIDExists(id):
            id_dict = cls.dictionary.get(id, None)
            if id_dict is not None:
                return id_dict
            else:
                ac_type = ActivityDB().fetch_attr('type', id)
                cls.dictionary[id] = cls.databaseDispatcher(id, ac_type)
                return cls.dictionary[id]
        return None


if __name__ == "__main__":
    stuff = ActivityDictionary()
    database: ModuleCompleted_DB = stuff.getDatabase("MD0000")
    database2 = stuff.getDatabase("MD0000")
    print(database is database2)
    database.addStudentEntry(("STD001",))
    # stuff = ModuleCompleted_DB("MD0000")
    # stuff.addStudentEntry(("STD001",))
