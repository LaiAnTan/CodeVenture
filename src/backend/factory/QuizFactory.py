from config import DATA_FILE, ANSWER_FILE
from .ActivityFactory import ActivityFactory


class QuizFactory(ActivityFactory):

    """
    Factory class for quizzes.
    """

    def __init__(self, header, content, assets) -> None:
        """
        Initialises the class.
        """

        super().__init__(header, content, assets, 'Quiz')

        self.image_used = set()
        self.code_used = set()
        self.answer = []

    def build(self):
        """
        Builds the quiz.
        """
        self.prepare_folders()
        self.set_AssetDict()

        with open(f'{self.activity_folder_dir}/{DATA_FILE}', '+w') as self.data_fd:
            self.build_Header()
            self.build_question(self.data_fd, self.image_used, self.code_used)
            self.generate_Files(self.image_used, self.code_used)
            self.build_Link(self.data_fd)
        self.used_file_dir.append(f'{self.activity_folder_dir}/{DATA_FILE}')

        with open(f'{self.activity_folder_dir}/{ANSWER_FILE}', '+w') as self.answer_fd:
            self.build_answer(self.answer_fd)
        self.used_file_dir.append(f'{self.activity_folder_dir}/{ANSWER_FILE}')

        # disabled temporary
        self.add_EntrytoDatabase()
        self.clean_up()

    def build_question(self, to_where, used_image: set, used_code: set):
        """
        Builds a question in the quiz.
        """

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
        """
        Builds the answer to a question in the quiz.
        """

        answer_line = '\n'.join(map(str, self.answer))
        to_where.write(f"{answer_line}")
