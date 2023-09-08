import os
from  PIL import ImageTk, Image

## 0 - Challange, 1 - Module, 2 - Quiz
activitiestype = ["Challenge", "Module", "Quiz"]
data_file = "data.ilovemen"

class Activity:
	def	__init__(self, filename: str, ac_type: int) -> None:
		self.ModulePath = os.getcwd() + f"/Activities/{activitiestype[ac_type]}/" + filename + "/"
		self.content = []
		self.img_src = []
		self.img = []

		get_content = False
		get_img = False
		with open(self.ModulePath + data_file) as file:
			for line in file:
				line = line.strip('\n')
				if get_content:
					if line == "CONTENT-END":
						get_content = False
						continue
					self.content.append(line)
					continue

				if get_img:
					if line == "IMG-CONT-END":
						get_img = False
						continue
					self.img_src.append(line)
					continue

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
					case "CONTENT-START":
						get_content = True
					case "IMG-CONT-START":
						get_img = True

		self.cleanup()

	def cleanup(self):
		## not sure about the Image thing
		self.img = { x.split('-')[0] : Image.open(self.ModulePath + x.split('-')[1]) for x in self.img_src }

	def __str__(self):
		description_msg = ''.join(self.content)
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
			f"Description",
			"-" * line_len
		]
		data.extend(description)
		data.extend(
			[
				"-" * line_len,
				f"Images",
				"-" * line_len,
			]
		)
		data.extend(self.img_src)

		return "\n".join(data)

if __name__ == "__main__":
	FuckMe = Activity("MD0000", 1)
	print(FuckMe)