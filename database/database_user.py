import database.database_base as db

class UserDB(db.DBBase):

	"""
	Singleton class that handles users database operations
	"""

	"""
	I do not know why we need 2 parameters
	I do not know what is placeholder for
	I do not know why am i doing this
	"""
	@classmethod
	def __new__(cls, placeholder=None):
		return super(UserDB, cls).__new__("users",
				"""
				username text,
				password text,
				user_type text
				"""
			)

if __name__ == "__main__":
    pass
