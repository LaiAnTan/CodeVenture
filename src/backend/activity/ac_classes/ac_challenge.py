from .ac_activity import Activity


class Hints(Activity):

    """
    Hints class for displaying hints in challenges.
    """

    def __init__(self, filename: str) -> None:
        super().__init__(filename, Activity.AType["Challenge"])
        self.data_file = "hints"

        self.read_data_file()
        self.ParseContent()
        self.ParseSources()

    def RunActivity(self):
        pass


class Challange(Activity):
    def __init__(self, filename: str) -> None:
        super().__init__(filename, Activity.AType["Challenge"])

        self.read_data_file()
        self.ParseHeader()
        self.ParseContent()
        self.ParseSources()

        self.hints = Hints(filename)

    def __str__(self):
        description_msg = ''.join([x[1] for x in self.content])
        line_len = 32
        desc_len = 10

        description = [description_msg[(line_len * x):(line_len * (x + 1))]
                       for x in range(desc_len)]

        # string building
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
                "Sources",
                "-" * line_len,
                "Images"
            ]
        )
        data.extend(self.img.values())
        data.extend(
            [
                "-" * line_len,
                "Code Snippets",
                "-" * line_len,
            ]
        )
        data.extend(self.code.values())

        return "\n".join(data)


if __name__ == "__main__":
    test = Challange("CH0000")
    print(test)
