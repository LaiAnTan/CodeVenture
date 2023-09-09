class Achievements():
    """
    Class for managing achievements and their criteria.
    """

    def __init__(self):
        self.achievements = []

    def add_achievement(self, achievement_name: str, achievement_details: str, depending_criteria) -> None:
        """
        Adds achievements.

        achievement_name: Name of achievement.
        achievement_details: Details of achievement.
        depending_criteria: Required completed modules.
        """
        achievement = {
            'name': achievement_name,
            'details': achievement_details,
            'depending_criteria': depending_criteria,
            'passed': False
        }
        self.achievements.append(achievement)

    def check_achievements(self, current_completed) -> None:
        """
        Checks if achievement criteria has been met and marks as passed.

        current_completed: The current activity level.
        """
        for achievement in self.achievements:
            if not achievement['passed'] and self.met_criteria(achievement['Depending_criteria'], current_completed):
                achievement['passed'] = True
                print(f"Congratulations! You received the {achievement['name']}")

    def met_criteria(self, depending_criteria, current_completed) -> bool:
        """
        Check if the criteria for an achievement has been met.

        depending_criteria: Required completed modules
        current_completed: Number of current completed modules
        returns True if criteria met, False otherwise.
        """
        # idk what im doing
        # hopefully it's okay

        return current_completed >= depending_criteria
        

if __name__ == "__main__":
    # Example:

    achievements = Achievements()
    current_completed = 5

    # Adds an achievement
    achievements.add_achievement("Bronze Badge", "Complete 3 learning modules", 3)

    # Checks if the achievement's criteria has been met
    achievements.check_achievements(current_completed)
