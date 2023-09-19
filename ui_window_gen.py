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

def subscribePage(a: App, student: Student):
    from ui_subscribe import SubscribeWindow
    a.clean_frame()
    sub_win = SubscribeWindow(student)
    sub_win.FillFrames(a)

def studentProfileSetupPage(a: App, student: Student):
    from ui_student_profile_setup import StudentProfileSetupWindow
    a.clean_frame()
    stud_profile_setup_win = StudentProfileSetupWindow(student)
    stud_profile_setup_win.FillFrames(a)

def datePickerTopLevelPage(a: App):
    from ui_date_picker import DatePickerWindow
    date_picker = DatePickerWindow(a, a.main_frame)
    date_picker.FillFrames()
    date_picker.wait_window()
    return date_picker.getSelectedDate()

## these are in ac_window_gen
# def modulePage(a: App, module: Module):
# def quizPage(a: App, quiz: Quiz):
# def challengePage(a: App, challenge: Challenge):
