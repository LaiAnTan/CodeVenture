import customtkinter as ctk

from app import App
from challenge import Challange
from window_gen import selection_screen

from PIL import Image

from ide import IDE

from imagelabel import ImageLabelGen

class ChallangeWindow():
	def __init__(self, challenge: Challange):
		self.attempted_count = 0
		self.challenge = challenge

	def ImageHandler(self, content, max_img_width, attach_frame):
		if self.challenge.img.get(content):
			ret_widget = ImageLabelGen(
				self.challenge.ModulePath + self.challenge.img[content],
				max_img_width - 50,
				attach_frame
			).ImageLabelGen()
		else:
			ret_widget = ctk.CTkLabel(
				attach_frame,
				text=f"Error displaying image {content}",
				width=max_img_width,
				wraplength=max_img_width - 10,
			)
		return ret_widget

	def	FillFrames(self, attach: App):
		## header details -------------------------------------------

		header_frame = ctk.CTkFrame(
			attach.main_frame
		)

		challange_name = ctk.CTkLabel(
			header_frame,
			text=f"{self.challenge.id} {self.challenge.title}"
		)

		back_button = ctk.CTkButton(
			header_frame,
			text="Back",
			command=lambda : selection_screen(attach),
			width=20
		)

		challange_name.pack(
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

		content_frame_height = 460
		content_frame_width = 350

		## left side of the frame

		main_content_frame = ctk.CTkFrame(
			content_frame,
		)

		## buttons to switch between 3 frames, question, hint 

		main_content_options_frame = ctk.CTkFrame(
			main_content_frame,
			width=content_frame_width + 20,
			height=25,
		)

		question_button = ctk.CTkButton(
			main_content_options_frame,
			width=110,
			height=25,
			text="Question",
			command=self.__beep_hoop_change_button
		)

		hint_button = ctk.CTkButton(
			main_content_options_frame,
			width=110,
			height=25,
			text="Hints",
			command=self.__beep_hoop_change_button
		)

		solution_button = ctk.CTkButton(
			main_content_options_frame,
			width=110,
			height=25,
			text="Solution",
			command=self.__beep_hoop_change_button
		)

		question_button.grid(
			row=0,
			column=0,
			padx=5,
			pady=5
		)

		hint_button.grid(
			row=0,
			column=1,
			padx=5,
			pady=5
		)

		solution_button.grid(
			row=0,
			column=2,
			padx=5,
			pady=5
		)

		main_content_options_frame.grid(
			row=0,
			column=0,
			padx=5,
			pady=5
		)

		## main question frame

		main_showcontent_frame = ctk.CTkScrollableFrame(
			main_content_frame,
			width=content_frame_width,
			height=content_frame_height - 40
		)

		for index, content in enumerate(self.challenge.content):
			paragraph_frame = ctk.CTkFrame(
				main_showcontent_frame
			)

			match content[0]:
				case Challange.Content_Type.Paragraph:
					paragraph = ctk.CTkLabel(
						paragraph_frame,
						text=content[1],
						width=content_frame_width - 10,
						wraplength=content_frame_width - 20,
						anchor="w",
						justify="left"
					)

				case Challange.Content_Type.Image:
					paragraph = self.ImageHandler(
						content[1],
						content_frame_width,
						paragraph_frame
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
				pady=5
			)
		
		main_showcontent_frame.grid(
			row=1,
			column=0,
			padx=5,
			pady=5
		)

		main_content_frame.grid(
			row=0,
			column=0,
			padx=5,
			pady=5
		)

		## left side of the frame done

		## some optional side bar start -----------------------

		sidebar_width = 350
		sidebar_frame = ctk.CTkScrollableFrame(
			content_frame,
			width=sidebar_width,
			height=460
		)

		a_shitty_ide = IDE(
			sidebar_width,
			sidebar_frame,
			self.challenge.id.lower(),
			"ST000", ## will change later
			self.challenge.ModulePath
		)

		a_shitty_ide_frame = a_shitty_ide.setUpFrame()

		a_shitty_ide_frame.grid(
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
			text="Mark",
			width=150,
			command= lambda : self.__beep_boop_button(a_shitty_ide.getContents())
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

	def __beep_boop_button(self, codecontent):
		print("Checking answer...")
		print("Wee wOO wEE wOO Wee wOO")
		print(f"This was in codecontet = {codecontent}")
		self.attempted_count += 1

	def __beep_hoop_change_button(self):
		print("Not Implemented!")