import os
from PIL import ImageTk, Image
from enum import Enum
from abc import ABC, abstractmethod

class Activity(ABC):
	data_file = "data.ilovemen"

	class AType(Enum):
		Module = 1
		Challenge = 2
		Quiz = 3

	def	__init__(self, filename: str, ac_type: AType) -> None:
		self.ModulePath = os.getcwd() + f"/Activities/{ac_type.name}/" + filename + "/"
		self.content = []
		self.footer = []
		self.type = ac_type

		self.id = "null"
		self.title = "null"
		self.difficulty = "null"
		self.tag = []
		self.achievement = []
		self.up_level = []

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
		with open(self.ModulePath + Activity.data_file) as file:
			for line in file:
				line = line.strip('\n')
				match line:
					case "HEADER-START":
						self.__get_Headers(file)
					case "CONTENT-START":
						self.__get_Content(file)
					case "SOURCES-START":
						self.__get_Sources(file)

		# self.__cleanup()

	def __cleanup(self):
		## not sure about the Image thing
		self.img = { x.split('-')[0] : Image.open(self.ModulePath + x.split('-')[1]) for x in self.img_src }
		self.code = { x.split('-')[0] : x.split('-')[1] for x in self.img_src }

	def __str__(self):
		# this is actually meant for developers only
		# will implement prettier one later
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
			f"Contents",
			"-" * line_len
		]
		data.extend(description)
		data.extend(
			[
				"-" * line_len,
				f"Sources",
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