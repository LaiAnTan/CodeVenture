from enum import Enum
from config import ACTIVITY_DIR, DATA_FILE


class Activity():

    """
    Base class for activities.
    """
    class Content_Type(Enum):

        """
        Enum for content type.
        """

        Paragraph = 0
        Image = 1
        Code = 2

    class AType(Enum):

        """
        Enum for activity type.
        """

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

    def __init__(self, filename: str, ac_type: AType) -> None:
        """
        Initialises the class.
        """
        self.ModulePath = f"{ACTIVITY_DIR}/{ac_type.name}/{filename}"
        self.content: list[str] = []
        self.footer: list[str] = []
        self.headerbuffer: list[str] = []
        self.type = ac_type
        self.img = {}
        self.code = {}
        self.data_file = DATA_FILE
        self.warnings = []
        self.errors = []

        # header values
        self.id = ''
        self.title = ''
        self.difficulty = ''
        self.tag = []

    def SourcesExtractor(self, to_where: dict, stop: str,
                         delimiter: str = '-') -> None:
        """
        Extracts sources
        Expects a list with 2 values, each seperated by the delimiter
        """
        while len(self.footer):
            contents = self.footer.pop(0)
            if contents == stop:
                return
            values = contents.split(delimiter)

            if (len(values) < 2) or values[1] == '':
                self.warnings.append(
                    (
                        'SOURCES',
                        'Source asset has no value and will be ignored'
                    )
                )
                continue

            # failsafe if the picture name consist of delimiter
            to_where[values[0]] = delimiter.join(values[1:])

        self.warnings.append(
            (
                'SOURCES',
                f'Delimiter {stop} not found, parse ended prematurely'
            )
        )

    def ParseSources(self) -> None:
        """
        Parses sources located in footer.
        """
        while len(self.footer):
            contents = self.footer.pop(0)
            match contents:
                case "IMG-CONT-START":
                    self.SourcesExtractor(self.img,
                                          "IMG-CONT-END")
                case "CODE-CONT-START":
                    self.SourcesExtractor(self.code,
                                          "CODE-CONT-END")

    def ParseContent(self):
        """
        Parses content.
        """
        for index, content in enumerate(self.content):
            if content.find("<IMG-CONT>") == 0:
                content = content.removeprefix("<IMG-CONT>")

                if not content:
                    self.warnings.append(
                        (
                            'CONTENT',
                            f'Image Asset in line {index + 1} has no image ID associated to it and will be ignored'
                        )
                    )
                    continue

                self.content[index] = (Activity.Content_Type.Image, content)
            elif content.find("<CODE-CONT>") == 0:
                content = content.removeprefix("<CODE-CONT>")

                if not content:
                    self.warnings.append(
                        (
                            'CONTENT',
                            f'Code Asset in line {index + 1} has no code ID associated to it and will be ignored'
                        )
                    )
                    continue

                self.content[index] = (Activity.Content_Type.Code, content)
            else:
                self.content[index] = (Activity.Content_Type.Paragraph,
                                       content)

        # print(self.content)

    def ParseHeader(self):
        """
        Parses header.
        """
        for line in self.headerbuffer:
            kwarg = line.split('|')

            if len(kwarg) < 2:
                self.warnings.append(
                    (
                        'HEADER',
                        f'Keyword {kwarg[0]} has no content'
                    )
                )
                continue

            if kwarg[1] == '':
                self.warnings.append(
                    (
                        'HEADER',
                        f'Keyword {kwarg[0]} content is empty!'
                    )
                )

            match kwarg[0]:
                case "ID":
                    self.id = kwarg[1]
                case "TITLE":
                    self.title = kwarg[1]
                case "DIFFICULTY":
                    self.difficulty = kwarg[1].count('*')
                case "TAG":
                    self.tag = [x.strip() for x in kwarg[1].split(',')]
                case _:
                    self.warnings.append(
                        (
                            'HEADER',
                            f'Unidentified Keyword {{{kwarg[0]}}}'
                        )
                    )

        # check if all content is successfully parsed
        # god please bless this code

        header_content = [self.id, self.title, self.difficulty, self.tag]
        names = ['ID', 'Title', 'Difficulty', 'Tag']

        if all(header_content) is False:
            missing_names = [names[index] for index in
                             range(len(header_content)) if not
                             header_content[index]]
            self.warnings.append(
                (
                    'HEADER',
                    f'Header field is incomplete, missing {str(missing_names).strip("[]")}'
                )
            )

    def __get_Headers(self, file):
        """
        Extracts header portion of file.
        """
        for line in file:
            line = line.strip('\n')
            if line == "HEADER-END":
                break
            self.headerbuffer.append(line)

    def __get_Content(self, file):
        """
        Extracts content portion of file.
        """
        for line in file:
            line = line.strip('\n')
            if line == "CONTENT-END":
                break
            self.content.append(line)

    def __get_Sources(self, file):
        """
        Extracts sources portion of file.
        """
        for line in file:
            line = line.strip('\n')
            if line == "SOURCES-END":
                break
            self.footer.append(line)

    def read_data_file(self):
        """
        Reads the .dat file and seperates the file into header, content and
        footer sections.
        """
        try:
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
        except FileNotFoundError:
            self.errors.append('data.dat not found!')
            return False

    def __str__(self):
        """
        Dunder method for displaying info.
        """
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
            "Contents",
            "-" * line_len
        ]
        data.extend(description)
        data.extend(
            [
                "-" * line_len,
                "Footer",
                "-" * line_len,
            ]
        )
        data.extend(self.footer)

        return "\n".join(data)

    def getWarning(self):
        """
        Getter for warnings.
        """
        return self.warnings

    def getErrors(self):
        """
        Getter for errors.
        """
        return self.errors

    def getHeaders(self):
        """
        Getter for headers, returned in a tuple.
        """
        return (
            self.id,
            self.title,
            self.difficulty,
            self.tag,
        )

    def getContent(self):
        """
        Getter for content.
        """
        return self.content

    def getSources(self):
        """
        Getter for sources.
        """
        return (
            self.img,
            self.code
        )


if __name__ == "__main__":
    pass
