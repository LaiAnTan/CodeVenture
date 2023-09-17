from App import App
from user.user_student import Student

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

def studentMenuPage(a: App, student: Student):
    from ui_student_menu import StudentMenuWindow
    a.clean_frame()
    student_menu_win = StudentMenuWindow(student)
    student_menu_win.FillFrames(a)

def profilePage(a: App, student: Student):
    from ui_profile import ProfileWindow
    a.clean_frame()
    profile_win = ProfileWindow(student)
    profile_win.FillFrames(a)

def settingsPage(a: App, student: Student):
    from ui_settings import SettingsWindow
    a.clean_frame()
    settings_win = SettingsWindow(student)
    settings_win.FillFrames(a)

def loadingPage(a: App, student: Student, redirect: str, message: list = []):
    from ui_loading import LoadingMenu
    a.clean_frame()
    loading_win = LoadingMenu(student)
    loading_win.FillFrames(a, redirect, message)

# def modulePage(a: App, module: Module):
#     pass

# def quizPage(a: App, quiz: Quiz):
#     pass

# def challengePage(a: App, challenge: Challenge):
#     pass