from config import ACTIVITY_DIR, DATA_FILE
from .ActivityFactory import ActivityFactory
import shutil as sht
import os


class ModuleFactory(ActivityFactory):
    def __init__(self, header, content, assets) -> None:
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
