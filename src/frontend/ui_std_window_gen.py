from src.frontend.ui_app import App
from src.backend.user.user_student import Student


def loginPage(a: App):
    from .ui_login import LoginWindow
    a.clean_frame()
    LoginWindow(a).attach_elements()
    a.main_frame.grid(row=0, column=0)


def registerPage(a: App):
    from .ui_register import RegisterWindow
    a.clean_frame()
    RegisterWindow(a).attach_elements()
    a.main_frame.grid(row=0, column=0)


def studentMenuPage(a: App, student: Student):
    from .ui_student_menu import StudentMenuWindow
    a.clean_frame()
    StudentMenuWindow(student, a).attach_elements()
    a.main_frame.grid(row=0, column=0)


def profilePage(a: App, student: Student):
    from .ui_profile import ProfileWindow
    a.clean_frame()
    ProfileWindow(student, a).attach_elements()
    a.main_frame.grid(row=0, column=0)


def settingsPage(a: App, student: Student):
    from .ui_settings import SettingsWindow
    a.clean_frame()
    SettingsWindow(student, a).attach_elements()
    a.main_frame.grid(row=0, column=0)


def subscribePage(a: App, student: Student):
    from .ui_subscribe import SubscribeWindow
    a.clean_frame()
    SubscribeWindow(student, a).attach_elements()
    a.main_frame.grid(row=0, column=0)


def studentProfileSetupPage(a: App, student: Student):
    from .ui_student_profile_setup import StudentProfileSetupWindow
    a.clean_frame()
    StudentProfileSetupWindow(student, a).attach_elements()
    a.main_frame.grid(row=0, column=0)


def datePickerTopLevelPage(a: App):
    from .helper_windows.ui_date_picker import DatePickerWindow
    date_picker = DatePickerWindow(a)
    date_picker.show_window()
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
    from .std_windows.ui_std_module_window import ModuleWindow

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
