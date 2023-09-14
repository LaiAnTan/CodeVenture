import database.database_base as db

class StudentDB(db.DBBase):

    """
    Singleton class that handles student database operations

    Notes:
    completed_quiz and completed_challenge are comma-seperated strings
    containing names of activities a student has completed.
    """

    @classmethod
    def __new__(cls, placeholder=None):
        return super().__new__(
            "students",
            """
            username text,
            name text,
            email text,
            subscription integer,
            date_of_birth text,
            completed_quiz text,
            completed_challenge text
            """
            )

if __name__ == "__main__":
    pass