import customtkinter as ctk

from App import App

from ac_activity import Activity
from ac_module import Module
from ac_quiz import Quiz
from ac_challenge import Challange
from ac_selection_window import SelectionScreen

def	selection_screen(a: App):
    a.clean_frame()

    SelectionScreen.attach_elements(a)
    a.main_frame.grid(
        row = 0,
        column = 0,
    )

from ac_challenge_window import ChallangeWindow
from ac_quiz_window import QuizWindow
from ac_module_windows import ModuleWindow

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