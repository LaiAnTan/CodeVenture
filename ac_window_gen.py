import customtkinter as ctk

from App import App

from ac_selection_window import SelectionScreen
from user.user_student import Student

def	selection_screen(a: App, student: Student):
    a.clean_frame()
    SelectionScreen(student, a).attach_elements()
    a.main_frame.grid(row = 0, column = 0)

from ac_challenge_window import ChallangeWindow
from ac_quiz_window import QuizWindow
from ac_module_windows import ModuleWindow

from ac_activity import Activity
from ac_module import Module
from ac_quiz import Quiz
from ac_challenge import Challange

def dispatcher(activityID, activityType, a: App, student: Student):
    a.clean_frame()
    match activityType:
        case Activity.AType.Module.value:
            ModuleWindow(Module(activityID), student, a).FillFrames()
        case Activity.AType.Quiz.value:
            QuizWindow(Quiz(activityID), student, a).FillFrames()
        case Activity.AType.Challenge.value:
            ChallangeWindow(Challange(activityID), student, a).FillFrames()
    a.main_frame.grid(row=0, column=0)