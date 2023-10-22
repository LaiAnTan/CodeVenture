from src.frontend.ui_app import App
from src.backend.user.user_student import Student


def loginPage(a: App):
    from .ui_login import LoginWindow
    a.clean_frame()
    a.change_frame(LoginWindow(a))


def registerPage(a: App):
    from .ui_register import RegisterWindow
    a.clean_frame()
    a.change_frame(RegisterWindow(a))


def studentMenuPage(a: App, student: Student):
    from .ui_student_menu import StudentMenuWindow
    a.clean_frame()
    a.change_frame(StudentMenuWindow(student, a))


def profilePage(a: App, student: Student):
    from .ui_profile import ProfileWindow
    a.clean_frame()
    a.change_frame(ProfileWindow(student, a))


def settingsPage(a: App, student: Student):
    from .ui_settings import SettingsWindow
    a.clean_frame()
    a.change_frame(SettingsWindow(student, a))


def subscribePage(a: App, student: Student):
    from .ui_subscribe import SubscribeWindow
    a.clean_frame()
    a.change_frame(SubscribeWindow(student, a))


def studentProfileSetupPage(a: App, student: Student):
    from .ui_student_profile_setup import StudentProfileSetupWindow
    a.clean_frame()
    a.change_frame(StudentProfileSetupWindow(student, a))


def datePickerTopLevelPage(a: App):
    from .helper_windows.ui_date_picker import DatePickerWindow
    date_picker = DatePickerWindow(a)
    date_picker.show_window()
    date_picker.wait_window()
    return date_picker.getSelectedDate()


def displayActivitySelections(a: App, student: Student):
    from .std_windows.ui_std_selection_window import SelectionScreen
    a.clean_frame()
    a.change_frame(SelectionScreen(student, a))


def dispatcher(activityID, activityType, a: App, student: Student):
    from .std_windows.ui_std_challenge_window import ChallangeWindow
    from .std_windows.ui_std_quiz_window import QuizWindow
    from .std_windows.ui_std_module_window import ModuleWindow

    from src.backend.activity.ac_classes.ac_activity import Activity
    from src.backend.activity.ac_classes.ac_module import Module
    from src.backend.activity.ac_classes.ac_quiz import Quiz
    from src.backend.activity.ac_classes.ac_challenge import Challange

    a.clean_frame()
    match activityType:
        case Activity.AType.Module.value:
            App().change_frame(ModuleWindow(Module(activityID), student, a))
        case Activity.AType.Quiz.value:
            App().change_frame(QuizWindow(Quiz(activityID), student, a))
        case Activity.AType.Challenge.value:
            App().change_frame(ChallangeWindow(Challange(activityID), student, a))
