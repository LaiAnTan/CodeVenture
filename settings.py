from copy import copy

class Settings:

    """
    Class for storing user settings
    """

    def __init__(self, config_file):
        self.config_file = config_file

        with open(config_file, "r") as file:
            self.data = file.readlines()

    
    def getSettingValue(self, setting_name: str):
        for n, entry in enumerate(self.data):
            if entry.find(setting_name) == -1:
                continue
            return self.data[n].strip("\n").split("=")[1]

    def updateSetting(self, setting_name: str, value: str):

        for n, entry in enumerate(self.data):
            if entry.find(setting_name) == -1:
                continue
            self.data[n] = setting_name + "=" + value + "\n"
            break

        with open(self.config_file, "w") as file:
            file.writelines(self.data)
