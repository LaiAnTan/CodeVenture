from abc import ABC, abstractmethod
from config import ACTIVITY_DIR, DATA_FILE
from ..database.database_activity import ActivityDB
from ..database.database_base import DBBase
import shutil as sht
import os

class ActivityFactory(ABC):
    def __init__(self, header, content, assets, ac_type) -> None:
        super().__init__()

        self.id = header[0]
        self.content = content
        self.assets = assets

        self.activity_folder_dir = f'{ACTIVITY_DIR}/{ac_type}/{self.id}'

        self.header = header
        # serialize the tag list
        self.header[4] = str(self.header[4]).strip('[]').replace("'", '').replace(' ', '')

        self.image_dict = {}
        self.code_dict = {}

        self.id_name_image = {}
        self.id_name_code = {}

        self.image_count = 0
        self.code_count = 0

        self.data_fd = None

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

    @abstractmethod
    def build(self):
        pass

    def prepare_folders(self):
        """prepare the main activity folder"""
        try:
            os.mkdir(self.activity_folder_dir)
        except FileExistsError:
            pass

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


    def build_content(self, to_where, from_where, used_image: set[tuple], used_code: set[tuple]):
        """
        builds content in file specified in to_where (usually data.dat)

        saves assets used in used_image and used_code
        """
        to_where.write("CONTENT-START\n")
        for content in from_where:
            match content[0]:
                case 'paragraph':
                    to_where.write(f'{content[1]}')
                case 'asset':
                    content = content[1]
                    match content[0]:
                        case 'code':
                            id = self.code_dict.get(content)
                            to_where.write(f'<CODE-CONT>{id}')
                            used_code.add(content)
                        case 'image':
                            id = self.image_dict.get(content)
                            to_where.write(f'<IMG-CONT>{id}')
                            used_image.add(content)
                case _:
                    raise TypeError("Invalid Content Type")
            to_where.write('\n')
        to_where.write("CONTENT-END\n\n")


    def copy_over_image(self, image_data, image_id):
        """
        copies over image from directory in image_data into 
        activity folder with name specified in image_data
        """
        source_file = image_data[2]
        extension = image_data[2].split('.')[-1]
        new_name = f'{image_data[1]}.{extension}' if image_data else f'Image_{image_id}.{extension}'
        destination_file = f'{self.activity_folder_dir}/{new_name}'

        sht.copy(source_file, destination_file)

        self.id_name_image[image_id] = new_name


    def make_code_dir(self, code_data, code_id):
        """
        makes the code directory
        with python code stored in code_data
        and input stored in code_data
        """
        code_name = code_data[1] if code_data[1] else f'Code_{code_id}'
        code_dir = f'{self.activity_folder_dir}/{code_name}'
        code_buffer = code_data[2]
        input_buffer = code_data[3]

        if not os.path.isdir(code_dir):
            os.mkdir(code_dir)

        # transfer code buffer into main.py
        with open(f'{code_dir}/main.py', '+w') as main_fd:
            main_fd.write(code_buffer)

        if input_buffer is not None:
            # transfer input buffer into input file
            with open(f'{code_dir}/input', '+w') as input_fd:
                input_fd.write(input_buffer)

        self.id_name_code[code_id] = code_name


    def add_EntrytoDatabase(self):
        """
        adds activity to database
        """
        print(tuple(self.header))
        try:
            ActivityDB().add_entry(tuple(self.header))
        except DBBase.DuplicateEntryException:
            ActivityDB().remove_entry(self.id)
            ActivityDB().add_entry(tuple(self.header))


    def generate_Files(self, used_image: set[tuple], used_code: set[tuple]):
        """
        generates images and code used in the content

        used image and used code is specified in used_image
        and used_code respectively

        generated files will be saved in self.id_name_image and
        self.id_name_code. Clear that two once you are done
        """
        print('[LOG]: Generating Required Files...')

        # image
        for used_content in used_image:
            self.copy_over_image(used_content, self.image_dict[used_content])

        # code
        for used_content in used_code:
            self.make_code_dir(used_content, self.code_dict[used_content])


    def build_Link(self, to_where):
        """
        builds footer data based on self.id_name_image and
        self.id_name_code
        """
        to_where.write("SOURCES-START\n")
        to_where.write("IMG-CONT-START\n")

        for id, name in self.id_name_image.items():
            to_where.write(f'{id}-{name}\n')

        to_where.write("IMG-CONT-END\n")
        to_where.write("CODE-CONT-START\n")

        for id, name in self.id_name_code.items():
            to_where.write(f'{id}-{name}\n')

        to_where.write("CODE-CONT-END\n")
        to_where.write("SOURCES-END\n\n")

