class Achievements:
    """
    Class for managing achievements and their criteria.
    """
    
    # Activate this class after completing an activity.
    # And for display on profile?

    # Class attributes for Bronze, Silver, and Gold badges
    all_achievements = [
        ["Achievement Name", "Details", "Criteria", "Status"],

        ["Module Completer: Bronze", "Complete 5 learning modules", 5, False],
        ["Module Completer: Silver", "Complete 15 learning modules", 15, False],
        ["Module Completer: Gold", "Complete 30 learning modules ", 30, False],

        ["Challenge Finisher: Bronze", "Complete 5 challenges", 5, False],
        ["Challenge Finisher: Silver", "Complete 15 challenges", 15, False],
        ["Challenge Finisher: Gold", "Complete 30 challenges", 30, False],
        
        ["Quiz Mastery: Bronze", "Successfully pass 5 quizzes", 5, False],
        ["Quiz Mastery: Silver", "Successfully pass 15 quizzes", 15, False],
        ["Quiz Mastery: Gold", "Successfully pass 30 quizzes", 30, False],      
    ]

    def __init__(self, achievement_name: str, achievement_details: str, depending_criteria: int, achievement_status = False) -> None:
        
        self.name = achievement_name
        self.details = achievement_details
        self.criteria = depending_criteria
        self.status = achievement_status
        self.display_achieved = []

        # self.completed_m = completed_modules
        # self.completed_c = completed_challenges
        # self.completed_q = completed_quizzes


    def set_status(self, status: bool) -> None:
        """
        Sets the status of an achievement to True if criteria met.
        Args:
            status (bool): True if achievement criteria met, False otherwise.
        """
        if status:
            self.status = True
            self.add_achievement(self.name)


    def add_achievement(self, achievement_name: str) -> None:
        """
        Appends an achievement to the achieved list.
        Args:
            achievement_name (str): Name of the achievement to be added to the list.
        """
        self.display_achieved.append(achievement_name)


    def met_criteria(self, current_completed: int) -> bool:
        """
        Check if the criteria for an achievement has been met.
        Args:
            current_completed (int): Number of current completed activities.
        Ret:
            bool: True if criteria met, False otherwise.
        """
        return current_completed >= self.criteria


    def check_achievements(self, current_completed: int) -> None:
        """
        Checks if achievement criteria has been met and marks as passed.
        Args:
            current_completed (int): The current activity level.
        """
        if not self.status and self.met_criteria(current_completed):
            self.set_status(True)
            print(f"Congratulations! You received the {self.name}")



if __name__ == "__main__":
    # Example:
    achievements = Achievements("Module Completer: Bronze", "Complete 5 learning modules", 5, False)
    current_completed = 5

    # Checks if the achievement's criteria has been met
    achievements.check_achievements(current_completed)

    # Display achieved achievements
    print("Achieved Achievements:", achievements.display_achieved)