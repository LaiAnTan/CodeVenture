import customtkinter as ctk

from app import App
from challenge import Challange
from window_gen import selection_screen

from PIL import Image

from ide import IDE

from imagelabel import ImageLabelGen

from code_runner import CodeRunner

class ChallangeWindow():
	def __init__(self, challenge: Challange):
		self.attempted_count = 0
		self.challenge = challenge
		self.main_showcontent_frame = None
		self.shittyIDE = None

	def ImageHandler(self, source, content, max_img_width, attach_frame):
		if source.img.get(content):
			ret_widget = ImageLabelGen(
				source.ModulePath + source.img[content],
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

	def QuestionFrames(self, frame_width):
		for widget in self.main_showcontent_frame.winfo_children():
			widget.destroy()
		self.main_showcontent_frame.forget()

		for index, content in enumerate(self.challenge.content):
			paragraph_frame = ctk.CTkFrame(
				self.main_showcontent_frame
			)

			match content[0]:
				case Challange.Content_Type.Paragraph:
					paragraph = ctk.CTkLabel(
						paragraph_frame,
						text=content[1],
						width=frame_width - 10,
						wraplength=frame_width - 20,
						anchor="w",
						justify="left"
					)

				case Challange.Content_Type.Image:
					paragraph = self.ImageHandler(
						self.challenge,
						content[1],
						frame_width,
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

	def	SolutionFrames(self, frame_width):
		for widget in self.main_showcontent_frame.winfo_children():
			widget.destroy()
		self.main_showcontent_frame.forget()

		if self.attempted_count > 5:
			solution_widget = CodeRunner(
				frame_width - 30,
				self.main_showcontent_frame,
				"solution.py",
				self.challenge.ModulePath
			).setUpFrame()
		else:
			solution_widget = ctk.CTkLabel(
						self.main_showcontent_frame,
						text="ERROR: Attempt More Times to Unlock the Solution!",
						width=frame_width - 10,
						wraplength=frame_width - 20,
						anchor="w",
						justify="left",
						text_color="red",
					)

		solution_widget.grid(
			row=0,
			column=0,
			padx=5,
			pady=5
		)

	def HintFrames(self, frame_width):
		for widget in self.main_showcontent_frame.winfo_children():
			widget.destroy()

		for index, content in enumerate(self.challenge.hints.content):
			paragraph_frame = ctk.CTkFrame(
				self.main_showcontent_frame
			)

			match content[0]:
				case Challange.Content_Type.Paragraph:
					paragraph = ctk.CTkLabel(
						paragraph_frame,
						text=content[1],
						width=frame_width - 10,
						height=10,
						wraplength=frame_width - 20,
						anchor="w",
						justify="left"
					)

				case Challange.Content_Type.Image:
					paragraph = self.ImageHandler(
						self.challenge.hints,
						content[1],
						frame_width,
						paragraph_frame
					)
			
			paragraph.grid(
				row=0,
				column=0,
			)

			paragraph_frame.grid(
				row=index,
				column=0,
				pady=5
			)

	def RunTestCases(self):
		own_code = self.shittyIDE.RunTestCases("test.in")
		test_code = CodeRunner(None, None, "solution.py", self.challenge.ModulePath).RunTestCases("test.in")
		if own_code == test_code:
			return True, own_code, test_code
		else:
			return False, own_code, test_code

	def RunTestCases_GenFrame(self, frame_width):
		self.attempted_count += 1
		result, usr_out, sys_out = self.RunTestCases()

		for widget in self.main_showcontent_frame.winfo_children():
			widget.destroy()

		if result == True:
			result = ctk.CTkLabel(
				self.main_showcontent_frame,
				text="OK!",
				text_color="limegreen",
				font=ctk.CTkFont(
					"Noto Sans Mono",
					size=25
				)
			)
		else:
			result = ctk.CTkLabel(
				self.main_showcontent_frame,
				text="KO!",
				text_color="red",
				font=ctk.CTkFont(
					"Noto Sans Mono",
					size=25
				)
			)

		result.grid(
			row=0,
			column=0,
			padx=5,
			pady=5
		)

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
			height=95,
		)

		question_button = ctk.CTkButton(
			main_content_options_frame,
			width=85,
			height=25,
			text="Question",
			command=lambda : self.QuestionFrames(content_frame_width)
		)

		hint_button = ctk.CTkButton(
			main_content_options_frame,
			width=85,
			height=25,
			text="Hints",
			command=lambda : self.HintFrames(content_frame_width)
		)

		solution_button = ctk.CTkButton(
			main_content_options_frame,
			width=85,
			height=25,
			text="Solution",
			command=lambda : self.SolutionFrames(content_frame_width)
		)

		mark_button = ctk.CTkButton(
			main_content_options_frame,
			width=85,
			height=25,
			text="Run Tests",
			command=lambda : self.RunTestCases_GenFrame(content_frame_width)
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

		mark_button.grid(
			row=0,
			column=3,
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

		self.main_showcontent_frame = ctk.CTkScrollableFrame(
			main_content_frame,
			width=content_frame_width,
			height=content_frame_height - 40
		)

		self.QuestionFrames(content_frame_width)

		self.main_showcontent_frame.grid(
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

		self.shittyIDE = IDE(
			sidebar_width,
			sidebar_frame,
			self.challenge.id.lower(),
			"ST000", ## will change later
			self.challenge.ModulePath
		)

		a_shitty_ide_frame = self.shittyIDE.setUpFrame()

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
			command= lambda : self.__beep_boop_button(self.shittyIDE.getContents())
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

	def __beep_hoop_change_button(self):
		print("Not Implemented!")
