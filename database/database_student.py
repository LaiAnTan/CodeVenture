import database.database_base as db

class StudentDB(db.DBBase):

    """
    Singleton class that handles student database operations

    Notes:
    c_quiz, c_challenge, c_achievements are comma-seperated strings
    containing names of stuff a student has completed.
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
            subscription_end text,
            date_of_birth text,
            c_quiz text,
            c_challenge text
            c_achievements text
            """
            )

if __name__ == "__main__":
    pass