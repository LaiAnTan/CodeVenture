import os
from enum import Enum
from abc import ABC, abstractmethod
from config import ACTIVITY_DIR, DATA_FILE

class Activity(ABC):
    class Content_Type(Enum):
        Paragraph = 0
        Image = 1
        Code = 2

    class AType(Enum):
        Module = 1
        Challenge = 2
        Quiz = 3

        def getSubScript(self):
            match self.value:
                case 1:
                    return 'MD'
                case 2:
                    return 'CH'
                case 3:
                    return 'QZ'

    def	__init__(self, filename: str, ac_type: AType) -> None:
        self.ModulePath = f"{ACTIVITY_DIR}/{ac_type.name}/{filename}"
        self.content: list[str] = []
        self.footer: list[str] = []
        self.type = ac_type
        self.img = {}
        self.code = {}
        self.data_file = DATA_FILE

        ## header values
        self.id = "null"
        self.title = "null"
        self.difficulty = "null"
        self.tag = []
        self.achievement = []
        self.up_level = []

    def SourcesExtractor(self, from_where: list[str], to_where: dict, stop: str, delimiter: str='-') -> None:
        """
        Extracts sources
        Expects a list with 2 values, each seperated by the delimiter
        """
        while len(self.footer):
            contents = self.footer.pop(0)
            if contents == stop:
                break
            values = contents.split(delimiter)
            to_where[values[0]] = values[1]

    def ParseSources(self) -> None:
        while len(self.footer):
            contents = self.footer.pop(0)
            match contents:
                case "IMG-CONT-START":
                    self.SourcesExtractor(self.footer, self.img, "IMG-CONT-END")
                case "CODE-CONT-START":
                    self.SourcesExtractor(self.footer, self.code, "CODE-CONT-END")

        # self.img = { x.split('-')[0] : Image.open(self.ModulePath + x.split('-')[1]) for x in self.img_src }
        # self.code = { x.split('-')[0] : x.split('-')[1] for x in self.img_src }

    def ParseContent(self):
        for index, content in enumerate(self.content):
            if content.find("<IMG-CONT>") == 0:
                content = content.removeprefix("<IMG-CONT>")
                self.content[index] = (Activity.Content_Type.Image, content)
            elif content.find("<CODE-CONT>") == 0:
                content = content.removeprefix("<CODE-CONT>")
                self.content[index] = (Activity.Content_Type.Code, content)
            else:
                self.content[index] = (Activity.Content_Type.Paragraph, content)

        # print(self.content)

    def	__get_Headers(self, file):
        for line in file:
            line = line.strip('\n')
            if line == "HEADER-END":
                break

            stuff = line.split("|")
            match stuff[0]:
                case "A_ID":
                    self.id = stuff[1]
                case "TITLE":
                    self.title = stuff[1]
                case "DIFFICULTY":
                    self.difficulty = stuff[1].count('*')
                case "TAG":
                    self.tag = stuff[1].split(',')
                case "ACHIEVEMENT":
                    self.achievement = stuff[1]
                case "UP_LEVEL":
                    self.up_level = stuff[1].split(',')

    def	__get_Content(self, file):
        for line in file:
            line = line.strip('\n')
            if line == "CONTENT-END":
                break
            self.content.append(line)

    def __get_Sources(self, file):
        for line in file:
            line = line.strip('\n')
            if line == "SOURCES-END":
                break
            self.footer.append(line)

    def read_mf_read(self):
        with open(f"{self.ModulePath}/{self.data_file}") as file:
            for line in file:
                line = line.strip('\n')
                match line:
                    case "HEADER-START":
                        self.__get_Headers(file)
                    case "CONTENT-START":
                        self.__get_Content(file)
                    case "SOURCES-START":
                        self.__get_Sources(file)

    def __str__(self):
        # this is actually meant for developers only
        # will implement prettier one later
        description_msg = ''.join(self.content)
        line_len = 32
        desc_len = 10

        description = []
        for x in range(desc_len):
            to_append = description_msg[(line_len * x):(line_len * (x + 1))]
            if not to_append:
                break
            description.append(to_append)

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
        data.extend(description)
        data.extend(
            [
                "-" * line_len,
                f"Footer",
                "-" * line_len,
            ]
        )
        data.extend(self.footer)

        return "\n".join(data)

    @abstractmethod
    def	RunActivity(self):
        pass

if __name__ == "__main__":
    pass