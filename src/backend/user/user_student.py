from ..user.user_base import User
from ..database.database_student import StudentDB


class Student(User):

    """
    Class that handles all operations as a student.
    """

    user_type = "student"

    def __init__(self, username):
        """
        Initializes the Student class that is inherited from user.
        """
        super().__init__(username)

        # query from student db
        db = StudentDB()

        if db.fetch_attr("username", self.username) == None:
            self.profile_setup = True
            return

        self.profile_setup = False
        self.name = db.fetch_attr("name", self.username)
        self.email = db.fetch_attr("email", self.username)
        self.subscription_status = db.fetch_attr("subscription", self.username)
        self.subscription_end_date = db.fetch_attr("subscription_end", self.username)
        self.dob = db.fetch_attr("date_of_birth", self.username)
        self.c_quiz = None
        self.c_challenge = None
        self.c_achievement = None

        # convert comma seperated string to values
        c_quiz_str = db.fetch_attr("c_quiz", self.username)
        if c_quiz_str:
            self.c_quiz = self.CSSToList(c_quiz_str)

        c_challenge_str = db.fetch_attr("c_challenge", self.username)
        if c_challenge_str:
            self.c_challenge = self.CSSToList(c_challenge_str)

        c_achievement_str = db.fetch_attr("c_achievement", self.username)
        if c_achievement_str:
            self.c_achievement = self.CSSToList(c_achievement_str)

    def __str__(self):
        """
        String dunder method returning the str representation of a student's
        details.
        """
        return f"""
--Student details--
username: {self.username}
name: {self.name}
email: {self.email}
subscription:  {self.subscription_status}
subscription end date: {self.subscription_end_date}
date of birth: {self.dob}
"""

    """
    Getters
    """

    def getUsername(self):
        return self.username

    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def getSubscriptionStatus(self):
        return "Active" if self.subscription_status == 1 else "Inactive"

    def getSubscriptionEndDate(self):
        return self.subscription_end_date

    def getDateOfBirth(self):
        return self.dob

    def getProfileSetupStatus(self):
        """
        Returns true if profile is not setup
        """
        return self.profile_setup

    """
    Methods
    """

    def isSubscribed(self):
        return True if self.subscription_status == 1 else False

    def CSSToList(self, c_sep_str):
        """
        Converts a comma seperated string into a list of values.

        @return values: list of values
        """
        return [val for val in c_sep_str.split(",")]
