import database as db

class StudentDB(db.DBBase):

	"""
	Singleton class that handles student database operations
	"""

	@classmethod
	def __new__(cls, placeholder=None):
		return super().__new__(
			"students",
			"""
			username text,
			subscription integer,
			date_of_birth text,
			quiz_results text,
			challenge_results texxt
			"""
			)

if __name__ == "__main__":
	pass