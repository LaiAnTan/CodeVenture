import database as db

class UserDB(db.DBBase):

	"""
	Singleton class that handles users database operations
	"""

	@classmethod
	def instance(cls):
		return super().instance(
			"users",
			"""
			username text,
			password text,
			user_type text
			"""
		)

if __name__ == "__main__":
	pass