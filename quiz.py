import activity as ac

class Question():
    def __init__(self, question_block: list[str]):
        self.id = question_block.pop(0).split('|')[1]
        self.prompt = []
        self.options = []

        self.__get_values(question_block)

    def __get_values(self, q_block: list[str]):
        while len(q_block):
            content = q_block.pop(0)
            if content == "OPTION":
                content = q_block.pop(0)
                self.options = content.split('|')
            else:
                self.prompt.append(content)

    def __str__(self):
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
        data.extend( [ "-" * line_len ] )

        return "\n".join(data)

    def	get_ID(self):
        return self.id
    
    def get_Prompt(self):
        return "\n".join(self.prompt)
    
    def get_Options(self):
        return self.options

class Quiz(ac.Activity):
    answer_sheet = "answer.ans"

    def __init__(self, filename: str) -> None:
        self.answers = {}
        self.questions: list[Question] = []

        super().__init__(filename, ac.Activity.AType["Quiz"])
        self.read_mf_read()
        self.__init_Questions()
        self.__getAnswers()

    def __getAnswers(self) -> None:
        with open(self.ModulePath + Quiz.answer_sheet) as file:
            for count, line in enumerate(file):
                self.answers[count] = line.strip('\n')

    def	__init_Questions(self) -> None:
        start = 0
        stop = 0
        while start < len(self.content):
            if self.content[start].split('|')[0] == "QUESTION":
                stop = self.content.index("QUESTION-END", start)
                self.questions.append(Question(self.content[start:stop]))
                start = stop
            start += 1
    
    def __str__(self):
        line_len = 32

        data = [
            f"{self.id} Module Description",
            "-" * line_len,
            f"Title = {self.title}",
            f"Difficulty = {self.difficulty}",
            f"Associated Tags = {str(self.tag).strip('[]')}",
            "-" * line_len,
            f"Contents",
            "-" * line_len
        ]
        data.extend([str(x) for x in self.questions])
        data.extend(
            [
                "-" * line_len,
                f"Answers",
                "-" * line_len
            ]
        )
        data.extend([f"{question} - {answer}" for question, answer in self.answers.items()])

        return "\n".join(data)

    def RunActivity(self):
        print("Running Quiz...")

if __name__ == "__main__":
    test = Quiz("QZ0000")
    print(test)
    pass