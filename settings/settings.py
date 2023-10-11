

class Settings:

    """
    Class for storing user settings (device specific)
    """

    def __init__(self, config_file):
        """
        Parses the file specified in config_file, into a list of settings.
        """
        self.config_file = config_file

        with open(config_file, "r") as file:
            self.data = file.readlines()

    def getSettingValue(self, setting_name: str):

        """
        Gets the setting value from self.data with name setting_name.
        """

        for n, entry in enumerate(self.data):
            if entry.find(setting_name) == -1:
                continue
            return self.data[n].strip("\n").split("=")[1]

    def updateSetting(self, setting_name: str, value: str):

        """
        Updates the setting value with name setting_name.
        """

        for n, entry in enumerate(self.data):
            if entry.find(setting_name) == -1:
                continue
            self.data[n] = setting_name + "=" + value + "\n"
            break

        with open(self.config_file, "w") as file:
            file.writelines(self.data)
