import customtkinter as ctk

from app import App
from quiz import Quiz
from window_gen import selection_screen

class QuizWindow():
	def	__init__(self, quiz: Quiz):
		self.quiz = quiz
	
	def	FillFrames(self, attach: App):
		header_frame = ctk.CTkFrame(
			attach.main_frame
		)

		back_button = ctk.CTkButton(
			header_frame,
			text="Back",
			command=lambda : selection_screen(attach),
			width=20
		)

		back_button.grid(
			row=0,
			column=0,
			padx=5,
			pady=5
		)

		header_frame.grid(
			row=0,
			column=0,
			sticky="e"
		)

		content_frame = ctk.CTkFrame(
			attach.main_frame,
			width=200,
			height=200
		)

		question_frames = []

		for index, questions in enumerate(self.quiz.questions):
			placeholder_frame = ctk.CTkFrame(
				content_frame
			)

			le_prompt = ctk.

			placeholder_frame.grid(
				row=index,
				column=0
			)

			question_frames.append((placeholder_frame, questions))

		content_frame.grid(
			row=1,
			column=0
		)

