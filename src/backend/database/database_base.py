import sqlite3 as sqlite3
import os

from config import DATABASE_DIR

class DBBase(object):

    """
    Singleton class that handles epic database for all your database needs
    """

    db_name = "unknown"
    db_path = "unknown"
    db_fields = "unknown"
    db_idfield = "unkown"
    db_placeholders = "placeholder text"
    conn = "placeholder text"
    cursor = "placeholder text"

    _instance = None
    BASE_DIR = DATABASE_DIR

    class DuplicateEntryException(Exception):
        """Called when trying to add entry that already exists in the
            database"""

        def __init__(self, msg="User already exists in the database"):
            super().__init__(msg)

    class EntryNotFoundException(Exception):
        """Called when trying to delete entry that does not exist in the
            database"""
        def __init__(self, msg="User not found in the database"):
            super().__init__(msg)

    class WrongDatatypeException(Exception):
        def __init__(self, msg="Value datatype does not match column"):
            super().__init__(msg)

    @classmethod
    def __new__(cls, db_name: str, fields: str):
        """
        Initializer for class variables
        """
        if cls._instance:
            return cls._instance
        cls._instance = super(DBBase, cls).__new__(cls)
        cls.db_name = db_name
        cls.db_path = os.path.join(cls.BASE_DIR, f"{cls.db_name}.db")
        cls.db_fields = fields

        # note: id_field is the first field in the database
        # it is used for as a primary key (unique identifier for each entry)
        cls.db_idfield = fields.split(",")[0].split()[0]

        # placeholder for field
        cls.db_placeholders = "(" + "".join(["?, " for _ in range(len(cls.db_fields.split(",")) - 1)]) + "?" + ")"

        # connection and cursor
        cls.conn = sqlite3.connect(cls.db_path)
        cls.cursor = cls.conn.cursor()

        # actually we abit funny one hor, why no init new db if dh db
        cls.new_db()
        return cls._instance

    @classmethod
    def __del__(cls):
        cls.conn.close()

    @classmethod
    def db_exists(cls):
        """
        checks if the database with name db_name currently exists
        """
        cls.cursor.execute(f"""SELECT tbl_name FROM sqlite_master WHERE
 type='table' AND tbl_name='{cls.db_name}'""")
        return cls.cursor.fetchone() is not None

    @classmethod
    def new_db(cls):
        """
        creates a new database with:
        - name specified in db_name
        - fields specified in db_fields
        (only works if the database doesnt currently exist)
        """
        if cls.db_exists() == False:
            cls.cursor.execute(f"CREATE TABLE {cls.db_name}({cls.db_fields})")
            cls.conn.commit()

    @classmethod
    def add_entry(cls, data: tuple):
        """
        adds a singular entry into the database

        Things to note:
        - placeholders (?) were used instead of named fields for easy addition
            of new fields
        - please ensure the first index of the data is a special id (primary /
            foreign key) for the data
        """
        if cls.fetch_attr(cls.db_idfield, data[0]) is not None:
            raise cls.DuplicateEntryException
        cls.cursor.execute(f"""INSERT INTO {cls.db_name} VALUES
 {cls.db_placeholders}""", data)
        cls.conn.commit()

    @classmethod
    def remove_entry(cls, data_id):
        """
        removes a singular entry from the database
        """
        if cls.fetch_attr(cls.db_idfield, data_id) is None:
            raise cls.EntryNotFoundException
        cls.cursor.execute(f"DELETE FROM {cls.db_name} WHERE {cls.db_idfield}=:{cls.db_idfield}", {cls.db_idfield: data_id})
        cls.conn.commit()

    @classmethod
    def fetch_attr(cls, field, data_id):
        """
        fetches the requested attribute from (field) that coressponds to entry
            with (data_id)
        returns None if the entry doesnt exist
        """
        # fetches the required attribute with the data that matches it
        # returns None if user not found
        value = cls.cursor.execute(f"SELECT {field} from {cls.db_name} WHERE {cls.db_idfield}=:{cls.db_idfield}", {cls.db_idfield: data_id}).fetchone()
        if value is None:
            return None
        else:
            return value[0]

    @classmethod
    def update_attr(cls, field, data_id, new_value):
        """
        updates the value in (field) that corresponds to entry with (data_id) with (new_value)

        raises EntryNotFoundException if the entry doesnt exist
        raises WrongDatatypeException if the datatype of new_value does not match the field
        """
        cls.cursor.execute(f"SELECT name, type FROM pragma_table_info('{cls.db_name}') WHERE name='{field}'")
        field_type = cls.cursor.fetchone()[1]

        match field_type:
            case "TEXT":
                if isinstance(new_value, str) == False:
                    raise cls.WrongDatatypeException
            case "INTEGER":
                if isinstance(new_value, int) == False:
                    raise cls.WrongDatatypeException
            case "REAL":
                if isinstance(new_value, float) == False:
                    raise cls.WrongDatatypeException

        if cls.fetch_attr(cls.db_idfield, data_id) == None:
            raise cls.EntryNotFoundException
        cls.cursor.execute(f"UPDATE {cls.db_name} SET {field}=:new_value WHERE {cls.db_idfield}=:{cls.db_idfield}", {'new_value':new_value, cls.db_idfield: data_id})
        cls.conn.commit()

    @classmethod
    def retrieve_all_attr(cls, data_id):
        """
        gets all the attributes for a certain entry with (data_id)
        """
        return cls.cursor.execute(f"SELECT * from {cls.db_name} WHERE {cls.db_idfield}=:{cls.db_idfield}", {cls.db_idfield: data_id}).fetchone()
