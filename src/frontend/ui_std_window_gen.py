from src.frontend.ui_app import App
from src.backend.user.user_student import Student


def loginPage():
    """
    Function that handles the frame switch to login window.
    """
    from .ui_login import LoginWindow
    App().clean_frame()
    App().change_frame(LoginWindow())


def registerPage():
    """
    Function that handles the frame switch to register window.
    """
    from .ui_register import RegisterWindow
    App().clean_frame()
    App().change_frame(RegisterWindow())


def studentMenuPage(student: Student):
    """
    Function that handles the frame switch to student menu window.
    """
    from .ui_student_menu import StudentMenuWindow
    App().clean_frame()
    App().change_frame(StudentMenuWindow(student))


def profilePage(student: Student):
    """
    Function that handles the frame switch to student profile window.
    """
    from .ui_profile import ProfileWindow
    App().clean_frame()
    App().change_frame(ProfileWindow(student))


def settingsPage(student: Student):
    """
    Function that handles the frame switch to settings window.
    """
    from .ui_settings import SettingsWindow
    App().clean_frame()
    App().change_frame(SettingsWindow(student))


def subscribePage(student: Student):
    """
    Function that handles the frame switch to subscribe window.
    """
    from .ui_subscribe import SubscribeWindow
    App().clean_frame()
    App().change_frame(SubscribeWindow(student))


def studentProfileSetupPage(student: Student):
    """
    Function that handles the frame switch to profile setup window.
    """
    from .ui_student_profile_setup import StudentProfileSetupWindow
    App().clean_frame()
    App().change_frame(StudentProfileSetupWindow(student))


def datePickerTopLevelPage():
    """
    Function that triggers the top level date picker window.
    """
    from .helper_windows.ui_date_picker import DatePickerWindow
    date_picker = DatePickerWindow()
    date_picker.show_window()
    date_picker.wait_window()
    return date_picker.getSelectedDate()


def displayActivitySelections(student: Student):
    """
    Function that handles the frame switch to activity selection window.
    """
    from .std_windows.ui_std_selection_window import SelectionScreen
    App().clean_frame()
    App().change_frame(SelectionScreen(student))


def dispatcher(activityID, activityType, student: Student, editor_view=False):
    """
    Function that handles the frame switch to the correct activity window.
    """

    from .std_windows.ui_std_challenge_window import ChallengeWindow
    from .std_windows.ui_std_quiz_window import QuizWindow
    from .std_windows.ui_std_module_window import ModuleWindow

    from ..backend.activity.ac_classes.ac_activity import Activity
    from ..backend.activity.ac_classes.ac_module import Module
    from ..backend.activity.ac_classes.ac_quiz import Quiz
    from ..backend.activity.ac_classes.ac_challenge import Challenge

    App().clean_frame()
    match activityType:
        case Activity.AType.Module.value:
            App().change_frame(ModuleWindow(Module(activityID), student))
        case Activity.AType.Quiz.value:
            App().change_frame(QuizWindow(Quiz(activityID), student))
        case Activity.AType.Challenge.value:
            App().change_frame(ChallengeWindow(Challenge(activityID), student))
