import pygments as pyg
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

from PIL import Image
from PIL.ImageOps import invert

import customtkinter as ctk

class CodeRunner():
	@classmethod
	def image_resizer(cls, image, max_width):
		width, height = image.size
		if width > max_width:
			height = ( height * max_width ) / width
			width = max_width
		return width, height

	@classmethod
	def	DisplayCodeline(cls, dictionary: dict, root_dir, content, max_img_width, attach_frame):
		if dictionary.get(content):
			code_content = []
			with open(root_dir + dictionary[content]) as file:
				for line in file:
					code_content.append(line)
			code_content = "".join(code_content)

			pyg.highlight(code_content,
				PythonLexer(),
				ImageFormatter(),
				outfile=f"{root_dir}temp.png"
			)

			image = Image.open(root_dir + "temp.png")
			size = cls.image_resizer(image, max_img_width - 50)

			ret_widget = ctk.CTkLabel(
				attach_frame,
				image=ctk.CTkImage(
					light_image=image,
					dark_image=invert(image),
					size=size
				),
				text=""
			)
		else:
			ret_widget = ctk.CTkLabel(
				attach_frame,
				text=f"Error displaying code {content}",
				width=max_img_width,
				wraplength=max_img_width - 10,
			)

		return ret_widget