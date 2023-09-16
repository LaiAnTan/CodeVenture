import activity as ac
from enum import Enum

class Module(ac.Activity):
    def __init__(self, filename: str) -> None:
        super().__init__(filename, ac.Activity.AType["Module"])
        self.read_mf_read()
        self.ParseContent()
        self.ParseSources()

    def RunActivity(self):
        print("Module Activity Running...")

    def __str__(self):
        description_msg = ''.join([x[1] for x in self.content])
        line_len = 32
        desc_len = 10

        description = [ description_msg[(line_len * x) : (line_len * (x + 1))] for x in range(desc_len) ]

        ## EPIC STRING BUILDING WOWOWOOWO
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
                f"Sources",
                "-" * line_len,
                f"Images"
            ]
        )
        data.extend(self.img.values())
        data.extend(
            [
                "-" * line_len,
                f"Code Snippets",
                "-" * line_len,
            ]
        )
        data.extend(self.code.values())

        return "\n".join(data)

if __name__ == "__main__":
    FuckMe = Module("MD0000")
    print(FuckMe)
    # FuckMe.RunActivity()