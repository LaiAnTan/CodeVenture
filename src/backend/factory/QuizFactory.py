"""
Quiz factory will not be as clean as the other two, too bad, so sad
"""

from .ActivityFactory import ActivityFactory
from config import DATA_FILE, ANSWER_FILE

class QuizFactory(ActivityFactory):
    def __init__(self, header, content, assets) -> None:
        super().__init__(header, content, assets, 'Quiz')

        self.image_used = set()
        self.code_used = set()
        self.answer = []


    def build(self):
        self.prepare_folders()
        self.set_AssetDict()

        with open(f'{self.activity_folder_dir}/{DATA_FILE}', '+w') as self.data_fd:
            self.build_Header()
            self.build_question(self.data_fd, self.image_used, self.code_used)
            self.generate_Files(self.image_used, self.code_used)
            self.build_Link(self.data_fd)
        
        with open(f'{self.activity_folder_dir}/{ANSWER_FILE}', '+w') as self.answer_fd:
            self.build_answer(self.answer_fd)

        # disabled temporary
        self.add_EntrytoDatabase()


    def build_question(self, to_where, used_image: set, used_code: set):
        to_where.write('CONTENT-START\n')
        for question in self.content:
            prompt = question[0]
            selection = question[1][1]
            answer = question[1][0]

            to_where.write('<QUESTION-START>\n')
            for segment in prompt:
                match segment[0]:
                    case 'paragraph':
                        to_where.write(f'{segment[1]}')
                    case 'asset':
                        asset_content = segment[1]
                        match asset_content[0]:
                            case 'code':
                                id = self.code_dict.get(asset_content)
                                to_where.write(f'<CODE-CONT>{id}')
                                used_code.add(asset_content)
                            case 'image':
                                id = self.image_dict.get(asset_content)
                                to_where.write(f'<IMG-CONT>{id}')
                                used_image.add(asset_content)
                to_where.write('\n')
            to_where.write('<OPTION>\n')
            to_where.write(f"{'|'.join(selection)}\n")
            to_where.write('<QUESTION-END>\n')

            self.answer.append(answer)

        to_where.write('CONTENT-END\n\n')

    def build_answer(self, to_where):
        answer_line = '\n'.join(map(str, self.answer))
        to_where.write(f"{answer_line}")