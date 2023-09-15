from App import App

def loginPage(a: App):
    from ui_login import LoginWindow
    a.clean_frame()
    login_win = LoginWindow()
    login_win.FillFrames(a)

def registerPage(a: App):
    from ui_register import RegisterWindow
    a.clean_frame()
    register_win = RegisterWindow()
    register_win.FillFrames(a)

from ui_student_menu import StudentMenuWindow
from user.user_student import Student

def studentMenuPage(a: App, student: Student):
    a.clean_frame()
    student_menu_win = StudentMenuWindow(student)
    student_menu_win.FillFrames(a)

from ui_profile import ProfileWindow

def profilePage(a: App, student: Student):
    a.clean_frame()
    profile_win = ProfileWindow(student)
    profile_win.FillFrames(a)

def settingsPage(a: App):
    pass

# def modulePage(a: App, module: Module):
#     pass

# def quizPage(a: App, quiz: Quiz):
#     pass

# def challengePage(a: App, challenge: Challenge):
#     pass