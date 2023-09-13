import pygments as pyg
import customtkinter as ctk
from PIL import Image

from app import App
from module import Module
from window_gen import selection_screen

class ModuleWindow():
	def	__init__(self, module: Module):
		self.module = module

	def image_resizer(self, image, max_width):
		width, height = image.size
		if width > max_width:
			height = ( height * max_width ) / width
			width = width
		return width, height
	
	def FillFrames(self, attach: App):

		## header details -------------------------------------------

		header_frame = ctk.CTkFrame(
			attach.main_frame
		)

		quiz_name = ctk.CTkLabel(
			header_frame,
			text=f"{self.module.id} {self.module.title}"
		)

		back_button = ctk.CTkButton(
			header_frame,
			text="Back",
			command=lambda : selection_screen(attach),
			width=20
		)

		quiz_name.pack(
			side=ctk.LEFT,
			padx=5,
			pady=5
		)

		back_button.pack(
			side=ctk.RIGHT,
			padx=5,
			pady=5
		)

		header_frame.grid(
			row=0,
			column=0,
			sticky="we",
			padx=5,
			pady=5
		)

		## header details end --------------------------------------------

		content_frame = ctk.CTkFrame(
			attach.main_frame,
		)

		## main_content frame ----------------------------

		main_content_frame_width = 550

		main_content_frame = ctk.CTkScrollableFrame(
			content_frame,
			width=main_content_frame_width,
			height=460
		)

		for index, content in enumerate(self.module.content):
			paragraph_frame = ctk.CTkFrame(
				main_content_frame
			)

			match content[0]:
				case Module.Content_Type.Paragraph:
					paragraph = ctk.CTkLabel(
						paragraph_frame,
						text=content[1],
						width=main_content_frame_width,
						wraplength=main_content_frame_width - 10,
						anchor="w",
						justify="left"
					)

				case Module.Content_Type.Image:
					if self.module.img.get(content[1]):
						image = Image.open(self.module.ModulePath + self.module.img[content[1]])
						size = self.image_resizer(image, main_content_frame_width - 50)

						paragraph = ctk.CTkLabel(
							paragraph_frame,
							image= ctk.CTkImage(
									light_image=image,
									size=size
								),
							text=""
						)
					else:
						paragraph = ctk.CTkLabel(
							paragraph_frame,
							text=f"Error displaying image {content[1]}",
							width=main_content_frame_width,
							wraplength=main_content_frame_width - 10,
						)

				case Module.Content_Type.Code:

					paragraph = ctk.CTkLabel(
						paragraph_frame,
						text="will display a image of a poorly formatted code here",
						width=main_content_frame_width,
						wraplength=main_content_frame_width - 10,
						anchor="w",
						justify="left"
					)

			paragraph.grid(
				row=0,
				column=0,
				padx=5,
				pady=5
			)

			paragraph_frame.grid(
				row=index,
				column=0,
				padx=5,
				pady=10
			)

		main_content_frame.grid(
			row=0,
			column=0,
			padx=5,
			pady=5
		)

		## qna frame end -------------------------------

		## some optional side bar start -----------------------

		sidebar_width = 50
		sidebar_frame = ctk.CTkFrame(
			content_frame,
			width=sidebar_width
		)

		some_label = ctk.CTkLabel(
			sidebar_frame,
			text="does module need a side bar tho....?",
			width=sidebar_width,
			wraplength=sidebar_width,
		)

		some_label.grid(
			row=0,
			column=0,
			padx=5,
			pady=5
		)

		sidebar_frame.grid(
			row=0,
			column=1,
			padx=5,
			pady=5
		)
		
		## some optional side bar end ----------------------------
		
		content_frame.grid(
			row=1,
			column=0,
			padx=5,
			pady=5,
		)

		## footer ---------------------------------------------

		footer_frame = ctk.CTkFrame(
			attach.main_frame,
		)

		submit_button = ctk.CTkButton(
			footer_frame,
			text="Complete",
			width=150,
			command= self.__beep_boop_button
		)

		submit_button.grid(
			row=0,
			column=0,
			padx=0,
			pady=0
		)

		footer_frame.grid(
			row=2,
			column=0,
			padx=5,
			pady=5
		)

		## footer end ------------------------------------------

	def __beep_boop(self, var):
		print("Value has changed = ", [x.get() for x in var])

	def __beep_boop_button(self):
		print("yeah yeah yeah setting it to completed... TRUST, WDYM IM NOT?")