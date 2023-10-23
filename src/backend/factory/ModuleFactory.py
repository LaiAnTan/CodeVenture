from config import ACTIVITY_DIR, DATA_FILE
from .ActivityFactory import ActivityFactory
from ..database.database_activity import ActivityDB
from ..database.database_base import DBBase
import shutil as sht
import os


class ModuleFactory(ActivityFactory):
    def __init__(self, header, content, assets) -> None:
        self.header = header
        # serialize the tag list
        self.header[4] = str(self.header[4]).strip('[]').replace("'", '').replace(' ', '')

        self.id = header[0]
        self.content = content
        self.assets = assets
        self.activity_folder_dir = f'{ACTIVITY_DIR}/Module/{self.id}'

        self.image_dict = {}
        self.code_dict = {}

        self.id_name_image = {}
        self.id_name_code = {}

        self.image_count = 0
        self.code_count = 0

        self.data_fd = None


    def build_Module(self):
        self.prepare_folders()
        self.set_AssetDict()

        # opens the new data file (data.dat)
        with open(f'{self.activity_folder_dir}/{DATA_FILE}', '+w') as self.data_fd:
            self.build_Header()
            self.build_Content()
            self.generate_Files()
            self.build_Link()

        self.add_EntrytoDatabase()

    # helper functions

    def set_AssetDict(self):
        """
        Set up image_dict and code_dict for assets
        Based on list of assets from self.asset

        All because ez id determination :D
        """

        for asset in self.assets:
            match asset[0]:
                case 'code':
                    if self.code_dict.get(asset) == None:
                        self.code_dict[asset] = f'CD{self.code_count:03d}'
                        self.code_count += 1
                case 'image':
                    if self.image_dict.get(asset) == None:
                        self.image_dict[asset] = f'IMG{self.image_count:03d}'
                        self.image_count += 1


    def prepare_folders(self):
        """prepare the main activity folder"""
        try:
            os.mkdir(self.activity_folder_dir)
        except FileExistsError:
            pass


    def build_Header(self):
        self.data_fd.write("HEADER-START\n")
        header_elements = {
            "ID": self.header[0],
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
                case 'asset':
                    content = content[1]
                    match content[0]:
                        case 'code':
                            self.data_fd.write(f'<CODE-CONT>{self.code_dict.get(content)}')
                        case 'image':
                            self.data_fd.write(f'<IMG-CONT>{self.image_dict.get(content)}')
                case _:
                    raise TypeError("Invalid Content Type")
            self.data_fd.write('\n')
        self.data_fd.write("CONTENT-END\n\n")


    def generate_Files(self):
        print('[LOG]: Generating Required Files...')

        for data, id in self.image_dict.items():
            self.copy_over_image(data, id)

        for data, id in self.code_dict.items():
            self.make_code_dir(data, id)


    def copy_over_image(self, image_data, image_id):
        source_file = image_data[2]
        extension = image_data[2].split('.')[-1]
        new_name = f'{image_data[1]}.{extension}' if image_data else f'Image-{image_id}.{extension}'
        destination_file = f'{self.activity_folder_dir}/{new_name}'

        sht.copy(source_file, destination_file)

        self.id_name_image[image_id] = new_name


    def make_code_dir(self, code_data, code_id):
        code_name = code_data[1] if code_data[1] else f'Code-{code_id}'
        code_dir = f'{self.activity_folder_dir}/{code_name}'
        code_buffer = code_data[2]
        input_buffer = code_data[3]

        if not os.path.isdir(code_dir):
            os.mkdir(code_dir)

        # transfer code buffer into main.py
        with open(f'{code_dir}/main.py', '+w') as main_fd:
            main_fd.write(code_buffer)

        # transfer input buffer into input file
        with open(f'{code_dir}/input', '+w') as input_fd:
            input_fd.write(input_buffer)

        self.id_name_code[code_id] = code_name

    def build_Link(self):
        self.data_fd.write("SOURCES-START\n")
        self.data_fd.write("IMG-CONT-START\n")

        for id, name in self.id_name_image.items():
            self.data_fd.write(f'{id}-{name}\n')

        self.data_fd.write("IMG-CONT-END\n")
        self.data_fd.write("CODE-CONT-START\n")

        for id, name in self.id_name_code.items():
            self.data_fd.write(f'{id}-{name}\n')

        self.data_fd.write("CODE-CONT-END\n")
        self.data_fd.write("SOURCES-END\n\n")


    def add_EntrytoDatabase(self):
        print(tuple(self.header))
        try:
            ActivityDB().add_entry(tuple(self.header))
        except DBBase.DuplicateEntryException:
            ActivityDB().remove_entry(self.id)
            ActivityDB().add_entry(tuple(self.header))
