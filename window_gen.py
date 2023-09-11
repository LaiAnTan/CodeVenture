import customtkinter as ctk

from app import App

from module import Module
from quiz import Quiz
from challenge import Challange
from selection_window import SelectionScreen

def	selection_screen(a: App):
	a.clean_frame()

	## make stuff centered
	a.main_frame.columnconfigure(
		(0, 1),
		weight=1
	)

	SelectionScreen.attach_elements(a)
	a.main_frame.grid(
		row = 0,
		column = 0,
	)

	## reset 
	a.main_frame.columnconfigure(
		(0, 1),
		weight=0
	)

from challenge_window import ChallangeWindow

def	challange_screen(challange: Challange, a: App):
	a.clean_frame()

	ChallangeWindow(challange).FillFrames(a)
	a.main_frame.place(
		relx=0.5,
		rely=0.5,
		anchor=ctk.CENTER
	)

from quiz_window import QuizWindow

def	quiz_screen(quiz: Quiz, a: App):
	a.clean_frame()

	QuizWindow(quiz).FillFrames(a)
	a.main_frame.place(
		relx=0.5,
		rely=0.5,
		anchor=ctk.CENTER
	)

from module_windows import ModuleWindow

def	module_screen(module: Module, a: App):
	a.clean_frame()

	ModuleWindow(module).FillFrames(a)
	a.main_frame.place(
		relx=0.5,
		rely=0.5,
		anchor=ctk.CENTER
	)