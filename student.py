from user import User

class Student(User):
    
    user_type = "student"
    
    def __init__(self, username):
        """
        Initializes the Student class that is inherited from User.
        """
        super().__init__(name, username)
        # query from db
        """
        self.student_id
        self.subscription_status
        self.stats: Stats
        self.dob
        self.quiz_results
        self.challenge_results
        """