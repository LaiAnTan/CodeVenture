from config import DATA_FILE
from .ActivityFactory import ActivityFactory


class ModuleFactory(ActivityFactory):

    """
    Factory class for modules.
    """

    def __init__(self, header, content, assets) -> None:

        """
        Initialises the class.
        """

        super().__init__(header, content, assets, 'Module')

        self.used_image = set()
        self.used_code = set()

    def build(self):
        self.prepare_folders()
        self.set_AssetDict()

        # opens the new data file (data.dat)
        with open(f'{self.activity_folder_dir}/{DATA_FILE}', '+w') as self.data_fd:
            self.build_Header()
            self.build_Data()
            self.generate_Data_Files()
            self.build_Data_Link()

        # disabled temporary
        self.add_EntrytoDatabase()

    # helper functions

    def build_Data(self):
        self.build_content(self.data_fd, self.content, self.used_image, self.used_code)

    def generate_Data_Files(self):
        self.generate_Files(self.used_image, self.used_code)

    def build_Data_Link(self):
        self.build_Link(self.data_fd)
