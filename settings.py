class Settings:

    """
    Class for storing user settings
    """

    def __init__(self):
        self.appearance_mode = "dark"
    
    """
    Getters
    """

    def getAppearanceMode(self):
        return self.appearance_mode

    """
    Methods
    """

    def swapAppearanceMode(self):
        
        if self.appearance_mode == "dark":
            self.appearance_mode = "light"

        elif self.appearance_mode == "light":
            self.appearance_mode = "dark"
    