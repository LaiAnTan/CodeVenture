import sqlite3 as sqlite3
import os

## haha funny attempt on inheritance
## pray i dont blow up and cry and die and distort
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
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))

	class DuplicateEntryException(Exception):
		"""Called when trying to add entry that already exists in the database"""
		
		def __init__(self, msg="User already exists in the database"):
			super().__init__(msg)
	
	class EntryNotFoundException(Exception):
		"""Called when trying to delete entry that does not exist in the database"""
		def __init__(self, msg="User not found in the database"):
			super().__init__(msg)

	@classmethod
	def	__new__(cls, db_name: str, fields: str):
		if cls._instance is None:
			cls._instance = super(DBBase, cls).__new__(cls)
			cls.db_name = db_name
			cls.db_path = os.path.join(cls.BASE_DIR, f"{cls.db_name}.db")
			cls.db_fields = fields
			
			# ensure that the id field is the first
			# i will distort if it isnt
			cls.db_idfield = fields.split(",")[0].split()[0]

			# placeholder for field
			cls.db_placeholders = "(" + "".join(["?, " for i in range(len(cls.db_fields.split(",")) - 1)]) + "?" + ")"

			# connection and cursor
			cls.conn = sqlite3.connect(cls.db_path)
			cls.cursor = cls.conn.cursor()
		return cls._instance

	@classmethod
	def db_exists(cls):
		"""
		checks if the database with name db_name currently exists
		"""
		cls.cursor.execute(f"""SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name='{cls.db_name}'""")
		return cls.cursor.fetchone() != None

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
		- placeholders (?) were used instead of named fields for easy addition of new fields
		- please ensure the first index of the data is a special id (primary / foreign key) for the data
		"""
		if cls.fetch_attr(cls.db_idfield, data[0]) != None:
			raise cls.DuplicateEntryException
		cls.cursor.execute(f"INSERT INTO {cls.db_name} VALUES {cls.db_placeholders}", data)
		cls.conn.commit()

	@classmethod
	def remove_entry(cls, data_id):
		"""
		removes a singular entry from the database
		"""
		if cls.fetch_attr("username", data_id) == None:
			raise cls.EntryNotFoundException
		cls.cursor.execute(f"DELETE FROM {cls.db_name} WHERE {cls.db_idfield}=:{cls.db_idfield}", {{cls.db_idfield}: data_id})
		cls.conn.commit()

	@classmethod
	def fetch_attr(cls, field, data_id):
		"""
		fetches the requested attribute from (field) that coressponds to entry with (data_id)
		returns None if the entry doesnt exist
		"""
		# fetches the required attribute with the data that matches it
		# returns None if user not found
		return cls.cursor.execute(f"SELECT {field} from {cls.db_name} WHERE {cls.db_idfield}=:{cls.db_idfield}", {cls.db_idfield: data_id}).fetchone()
