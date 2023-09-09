import database as db

class UserDB(db.DBBase):

	"""
	Singleton class that handles users database operations
	"""

	@classmethod
	def __new__(cls, db_name=None, db_fields=None):
		return super(UserDB, cls).__new__("users",
				"""
				username text,
				password text,
				user_type text
				"""
			)

if __name__ == "__main__":
	pass