import customtkinter as ctk

from app import App
from challenge import Challange
from window_gen import selection_screen

class ChallangeWindow():
	def __init__(self, challenge: Challange):
		self.challenge = challenge

	def	FillFrames(self, attach: App):
		back_button = ctk.CTkButton(
			attach.main_frame,
			text="Back",
			command=lambda : selection_screen(attach),
			width=20
		)

		back_button.grid(
			row=0,
			column=1,
			padx=5,
			pady=5
		)

		placeholder = ctk.CTkLabel(
			attach.main_frame,
			text="Wooo, imagine there is text here Woooo",
			text_color="black",
			fg_color="#D3D3D3",
			padx=120,
			pady=190
		)

		placeholder.grid(
			row=1,
			column=0,
			columnspan=1,
			padx=5,
			pady=5
		)
