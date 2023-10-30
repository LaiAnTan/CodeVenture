from .ActivityFactory import ActivityFactory
from config import DATA_FILE, HINT_FILE, TESTCASE_FOLDER
import os

class ChallengeFactory(ActivityFactory):
    def __init__(self, header, content, assets) -> None:
        super().__init__(header, content, assets, 'Challenge')

        self.data_content = content[0]
        self.solution = content[1]
        self.hints_content = content[2]
        self.testcases = content[3]

        # [[images], [codes]]
        self.asset_in_content: list[set[tuple]] = [set(), set()]
        self.asset_in_hints: list[set[tuple]] = [set(), set()]

    def build(self):
        self.prepare_folders()
        self.set_AssetDict()

        # build data.dat
        with open(f'{self.activity_folder_dir}/{DATA_FILE}', '+w') as self.data_fd:
            self.build_Header()
            self.build_Data()
            self.generate_Files(self.asset_in_content[0], self.asset_in_content[1])
            self.build_Link(self.data_fd)
        self.used_file_dir.append(f'{self.activity_folder_dir}/{DATA_FILE}')

        # clear stored image and code
        self.id_name_image.clear()
        self.id_name_code.clear()

        # build hint
        with open(f'{self.activity_folder_dir}/{HINT_FILE}', '+w') as self.hint_fd:
            self.build_Hint()
            self.generate_Files(self.asset_in_hints[0], self.asset_in_hints[1])
            self.build_Link(self.hint_fd)
        self.used_file_dir.append(f'{self.activity_folder_dir}/{HINT_FILE}')

        # build solution folder
        temp_buffer = ('code', 'solution', self.solution[0], self.solution[1])
        self.make_code_dir(temp_buffer, 'solution')

        # build test cases
        self.build_Testcase()

        self.add_EntrytoDatabase()
        self.clean_up()

    def build_Data(self):
        self.build_content(self.data_fd, self.data_content, self.asset_in_content[0], self.asset_in_content[1])

    def build_Hint(self):
        self.build_content(self.hint_fd, self.hints_content, self.asset_in_hints[0], self.asset_in_hints[1])

    def build_Testcase(self):
        for test_no, test_case in enumerate(self.testcases):
            with open(f'{self.activity_folder_dir}/{TESTCASE_FOLDER}/{test_no}', '+w') as fd:
                fd.write(test_case)
        self.used_file_dir.append(f'{self.activity_folder_dir}/{TESTCASE_FOLDER}')

    def prepare_folders(self):
        super().prepare_folders()

        # prepare the hints folder as well
        try:
            os.mkdir(f'{self.activity_folder_dir}/{TESTCASE_FOLDER}')
        except FileExistsError:
            pass
