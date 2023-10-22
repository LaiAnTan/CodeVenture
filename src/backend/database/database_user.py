from .database_base import DBBase


class UserDB(DBBase):

    """
    Singleton class that handles users database operations
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
