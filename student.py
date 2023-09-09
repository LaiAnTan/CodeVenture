from user import User
from database_student import StudentDB

# this class is only used if you logged in as a student

# handles everything a student does and also updates database respectively
class Student(User):
    
    user_type = "student"
    
    def __init__(self, username):
        """
        Initializes the Student class that is inherited from User.
        """
        super().__init__(name, username)
        
        # query from db
        db = StudentDB()
        self.id = db.fetch_attr("id", self.username)
        self.subciption_status = db.fetch_attr("subscription", self.username)
        self.dob = db.fetch_attr("date_of_birth", self.username)
        self.completed_quiz = db.fetch_attr("completed_quiz", self.username)
        self.completed_challenge = db.fetch_attr("completed_challenge", self.username)

        # convert completed_quiz & completed_challenge into dicts of QuizResult and ChallengeResult objects
