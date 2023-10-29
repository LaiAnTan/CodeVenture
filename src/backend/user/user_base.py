
from abc import ABC
from argon2 import PasswordHasher, exceptions

from ..database.database_user import UserDB


class User(ABC):

    def __init__(self, username):
        """
        Initializes the User abstract class.
        Note only the username is saved here,
        and will be used to query for other values in the backend.database.
        """
        self.username = username
        self.login_status = False
        self.user_type = None

    """
    Getters
    """
    def getUsername(self) -> str:
        return self.username

    def getUserType(self):
        return self.user_type

    """
    Setters
    """

    def setUsername(self, username: str) -> None:
        self.username = username

    """
    Methods
    """

    def login(self, pw_input) -> bool:
        """
        Function that authenticates user login.

        Tries to match pw_input with password from db
        """
        db = UserDB()

        ph = PasswordHasher()

        user_pw = db.fetch_attr("password", self.getUsername())
        if user_pw is None:  # user not in database
            return False

        try:
            ph.verify(user_pw, pw_input)
            self.login_status = True
            self.user_type = db.fetch_attr("user_type", self.getUsername())
            print(self.user_type)
            return True
        except exceptions.VerifyMismatchError:  # login failed
            return False

    def logout(self) -> bool:
        """
        Function that logs out a user.
        """
        self.login_status = False

    # @abstractmethod
    # def export_user_data():
    #     pass
