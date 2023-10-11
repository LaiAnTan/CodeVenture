from src.frontend.ui_app import App
from src.backend.user.user_student import Student


def loginPage(a: App):
    from .ui_login import LoginWindow
    a.clean_frame()
    LoginWindow(a).attach_elements()


def registerPage(a: App):
    from .ui_register import RegisterWindow
    a.clean_frame()
    register_win = RegisterWindow()
    register_win.FillFrames(a)


def studentMenuPage(a: App, student: Student):
    from .ui_student_menu import StudentMenuWindow
    a.clean_frame()
    student_menu_win = StudentMenuWindow(student)
    student_menu_win.FillFrames(a)


def profilePage(a: App, student: Student):
    from .ui_profile import ProfileWindow
    a.clean_frame()
    profile_win = ProfileWindow(student)
    profile_win.FillFrames(a)


def settingsPage(a: App, student: Student):
    from .ui_settings import SettingsWindow
    a.clean_frame()
    settings_win = SettingsWindow(student)
    settings_win.FillFrames(a)


def subscribePage(a: App, student: Student):
    from .ui_subscribe import SubscribeWindow
    a.clean_frame()
    sub_win = SubscribeWindow(student)
    sub_win.FillFrames(a)


def studentProfileSetupPage(a: App, student: Student):
    from .ui_student_profile_setup import StudentProfileSetupWindow
    a.clean_frame()
    stud_profile_setup_win = StudentProfileSetupWindow(student)
    stud_profile_setup_win.FillFrames(a)


def datePickerTopLevelPage(a: App):
    from .helper_windows.ui_date_picker import DatePickerWindow
    date_picker = DatePickerWindow(a, a.main_frame)
    date_picker.FillFrames()
    date_picker.wait_window()
    return date_picker.getSelectedDate()


def displayActivitySelections(a: App, student: Student):
    from .std_windows.ui_std_selection_window import SelectionScreen
    a.clean_frame()
    SelectionScreen(student, a).attach_elements()
    a.main_frame.grid(row=0, column=0)


def dispatcher(activityID, activityType, a: App, student: Student):
    from .std_windows.ui_std_challenge_window import ChallangeWindow
    from .std_windows.ui_std_quiz_window import QuizWindow
    from .std_windows.ui_std_module_windows import ModuleWindow

    from src.backend.activity.ac_classes.ac_activity import Activity
    from src.backend.activity.ac_classes.ac_module import Module
    from src.backend.activity.ac_classes.ac_quiz import Quiz
    from src.backend.activity.ac_classes.ac_challenge import Challange

    a.clean_frame()
    match activityType:
        case Activity.AType.Module.value:
            ModuleWindow(Module(activityID), student, a).Attach()
        case Activity.AType.Quiz.value:
            QuizWindow(Quiz(activityID), student, a).Attach()
        case Activity.AType.Challenge.value:
            ChallangeWindow(Challange(activityID), student, a).Attach()
    a.main_frame.grid(row=0, column=0)
