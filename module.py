import activity as ac
from enum import Enum

class Module(ac.Activity):

	class Content_Type(Enum):
		Paragraph = 0
		Image = 1
		Code = 2

	def __init__(self, filename: str) -> None:
		self.img = {}
		self.code = {}

		super().__init__(filename, ac.Activity.AType["Module"])
		self.read_mf_read()
		self.ParseContent()
		self.processSources()

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

	def processSources(self) -> None:
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
				self.content[index] = (Module.Content_Type.Image, content)
			elif content.find("<CODE-CONT>") == 0:
				content = content.removeprefix("<CODE-CONT>")
				self.content[index] = (Module.Content_Type.Code, content)
			else:
				self.content[index] = (Module.Content_Type.Paragraph, content)

		# print(self.content)

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