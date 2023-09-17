import customtkinter as ctk

from app import App

from activity import Activity
from module import Module
from quiz import Quiz
from challenge import Challange
from selection_window import SelectionScreen

def	selection_screen(a: App):
    a.clean_frame()

    SelectionScreen.attach_elements(a)
    a.main_frame.grid(
        row = 0,
        column = 0,
    )

from challenge_window import ChallangeWindow
from quiz_window import QuizWindow
from module_windows import ModuleWindow

def dispatcher(activityID, activityType, a: App):
    a.clean_frame()
    match activityType:
        case Activity.AType.Module.value:
            ModuleWindow(Module(activityID)).FillFrames(a)
        case Activity.AType.Quiz.value:
            QuizWindow(Quiz(activityID)).FillFrames(a)
        case Activity.AType.Challenge.value:
            ChallangeWindow(Challange(activityID)).FillFrames(a)

    a.main_frame.grid(row=0, column=0)