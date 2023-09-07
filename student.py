from user import User

class Student(User):
    
    def __init__(self, name, username, password):
        """
        Initializes the Student class that is inherited from User.
        """
        super().__init__(name, username)
        # not done