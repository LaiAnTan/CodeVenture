from config import ACTIVITY_DIR, DATA_FILE
from .ActivityFactory import ActivityFactory
from ..database.database_activity import ActivityDB
from ..database.database_base import DBBase
import os

class ModuleFactory(ActivityFactory):
    def __init__(self, header, content) -> None:
        self.header = header
        # serialize the tag list
        self.header[4] = str(self.header[4]).strip('[]').replace("'", '').replace(' ', '')

        self.id = header[0]
        self.content = content
        
        self.image_dict = {}
        self.image_count = 0
        self.code_dict = {}
        self.code_count = 0

        self.data_fd = None

    def build_Module(self):
        self.prepare_folders()

        # opens the new DATA_FILE
        with open(f'{self.ac_root_dir}/{DATA_FILE}', '+w') as self.data_fd:
            self.build_Header()
            self.build_Content()
            self.build_Link()

        self.generate_Files()
        self.add_EntrytoDatabase()

    # helper functions

    def prepare_folders(self):
        # prepare the main activity folder
        self.ac_root_dir = f'{ACTIVITY_DIR}/Module/{self.id}'
        try:
            os.mkdir(self.ac_root_dir)
        except FileExistsError:
            pass

    def build_Header(self):
        self.data_fd.write("HEADER-START\n")
        header_elements = {
            "A_ID": self.header[0],
            "TITLE": self.header[2],
            "DIFFICULTY": '*' * self.header[3],
            "TAG": self.header[4]
        }
        for key, value in header_elements.items():
            self.data_fd.write(f'{key}|{value}\n')
        self.data_fd.write("HEADER-END\n\n")

    def build_Content(self):
        self.data_fd.write("CONTENT-START\n")
        for content in self.content:
            match content[0]:
                case 'paragraph':
                    self.data_fd.write(f'{content[1]}')
                case 'code':
                    self.code_count += 1
                case 'image':
                    if self.image_dict.get((content[1], content[2])) == None:
                        self.image_dict[(content[1], content[2])] = f'IMG{self.image_count:03d}'
                        self.image_count += 1
                    self.data_fd.write(f'<IMG-CONT>{self.image_dict[(content[1], content[2])]}')
                case _:
                    raise TypeError("Invalid Content Type")
            self.data_fd.write('\n')
        self.data_fd.write("CONTENT-END\n\n")
        print(self.image_dict)

    def generate_Files(self):
        print('[LOG]: Generating Required Files...')
        pass

    def build_Link(self):
        self.data_fd.write("SOURCES-START\n")

        self.data_fd.write("SOURCES-END\n\n")

    def add_EntrytoDatabase(self):
        print(tuple(self.header))
        try:
            ActivityDB().add_entry(tuple(self.header))
        except DBBase.DuplicateEntryException:
            ActivityDB().remove_entry(self.id)
            ActivityDB().add_entry(tuple(self.header))