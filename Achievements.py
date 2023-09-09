class Achievements():
    """
    Class for managing achievements and their criteria.
    """
    
    # Class attributes for Bronze, Silver, and Gold badges
    bronze_badge = {
        'name': "Bronze Badge",
        'details': "Complete 5 learning modules",
        'criteria': 5
    }

    silver_badge = {
        'name': "Silver Badge",
        'details': "Complete 15 learning modules",
        'criteria': 15
    }

    gold_badge = {
        'name': "Gold Badge",
        'details': "Complete 30 learning modules",
        'criteria': 30
    }

    badges = [bronze_badge, silver_badge, gold_badge]

    def __init__(self):
        self.achievements = []

    def add_achievement(self, module_name: str, module_details: str, depending_criteria: int) -> None:
        """
        Adds achievements.

        module_name: Name of achievement.
        module_details: Details of achievement.
        depending_criteria: Required completed modules.
        """
        achievement = {
            'name': module_name,
            'details': module_details,
            'criteria': depending_criteria,
            'passed': False
            #'badge_image' : image?
        }

        self.achievements.append(achievement)


    def check_achievements(self, module_name: str, current_completed: int) -> None:
        """
        Checks if achievement criteria has been met and marks as passed.

        current_completed: The current activity level.
        """
        for achievement in Achievements.badges:
            if not achievement['passed'] and self.met_criteria(achievement['depending_criteria'], current_completed):
                achievement['passed'] = True
                print(f"Congratulations! You received the {achievement['name']} for the {module_name} module.")


    def met_criteria(self, depending_criteria: int, current_completed: int) -> bool:
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

    # Checks if the achievement's criteria has been met
    achievements.check_achievements(current_completed)