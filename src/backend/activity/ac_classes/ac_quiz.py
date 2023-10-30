from .ac_activity import Activity


class Question():

    """
    Class representing a singular question in a quiz.
    """

    def __init__(self, question_block: list[str], id):
        """
        Initialises the class.
        """
        self.id = id
        self.prompt: list[tuple[Activity.Content_Type, str]] = []
        self.options: list[str] = []

        self.__get_values(question_block)

    def __append_prompt(self, content: str):
        if content.find("<IMG-CONT>") == 0:
            content = content.removeprefix('<IMG-CONT>')
            data_chunk = (Activity.Content_Type.Image, content)
        elif content.find('<CODE-CONT>') == 0:
            content = content.removeprefix('<CODE-CONT>')
            data_chunk = (Activity.Content_Type.Code, content)
        else:
            data_chunk = (Activity.Content_Type.Paragraph, content)

        self.prompt.append(data_chunk)

    def __get_values(self, q_block: list[str]):
        while len(q_block):
            content = q_block.pop(0)
            if content == "<OPTION>":
                content = q_block.pop(0)
                self.options = content.split('|')
            else:
                self.__append_prompt(content)

    def __str__(self):
        """
        Dunder method to construct string representation of a question.
        """
        line_len = 32

        data = [
            f"Question -- {self.id}",
            "-" * line_len,
        ]
        data.extend(self.prompt)
        data.extend(
            [
                "-" * line_len,
                f"Options",
                "-" * line_len,
                ", ".join(self.options)
            ]
        )
        data.extend(["-" * line_len])

        return "\n".join(data)

    def get_ID(self):
        """
        Getter for id.
        """
        return self.id

    def get_Prompt(self):
        """
        Getter for prompt.
        """
        return self.prompt

    def get_Options(self):
        """
        Getter for options.
        """
        return self.options


class Quiz(Activity):

    """
    Quiz class to parse a quiz.
    """

    answer_sheet = "answer.ans"

    def __init__(self, filename: str) -> None:
        """
        Initialises the class.
        """

        self.answers = []
        self.questions: list[Question] = []

        super().__init__(filename, Activity.AType["Quiz"])
        self.read_data_file()
        self.ParseHeader()
        self.ParseSources()
        self.__init_Questions()
        self.__getAnswers()

    def getQuestionAnswer(self, index):
        """
        Get the answer for a specific question.
        """

        return self.answers[index]

    def checkAnswers(self, index, answer) -> bool:
        """
        Checks the answer of a specific question with the anwer passed as
        paremeter.

        True if correct, False if wrong.
        """

        return self.getQuestionAnswer(index) == answer

    def __getAnswers(self) -> None:
        """
        Extract the answers from a file.
        """

        with open(f"{self.ModulePath}/{Quiz.answer_sheet}") as file:
            for line in file:
                self.answers.append(int(line.strip()))

    def __init_Questions(self) -> None:
        """
        Extract the questions from a file.
        """

        start = 0
        stop = 0
        question_no = 0
        while start < len(self.content):
            if self.content[start] == "<QUESTION-START>":
                stop = self.content.index("<QUESTION-END>", start)
                self.questions.append(Question(self.content[start+1:stop], question_no))
                question_no += 1
                start = stop
            start += 1

    def __str__(self):
        """
        Dunder method to construct string representation of a quiz to be
        displayed.
        """

        line_len = 32

        data = [
            f"{self.id} Module Description",
            "-" * line_len,
            f"Title = {self.title}",
            f"Difficulty = {self.difficulty}",
            f"Associated Tags = {str(self.tag).strip('[]')}",
            "-" * line_len,
            "Contents",
            "-" * line_len
        ]
        data.extend([str(x) for x in self.questions])
        data.extend(
            [
                "-" * line_len,
                "Answers",
                "-" * line_len
            ]
        )
        data.extend([f"{question} - {answer}" for question, answer in self.answers.items()])

        return "\n".join(data)


if __name__ == "__main__":
    test = Quiz("QZ0000")
    print(test)
