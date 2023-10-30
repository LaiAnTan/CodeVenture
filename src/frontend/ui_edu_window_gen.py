from .ui_app import App


def dispatcher(option, existing_activity):
    """
    Function that handles the frame switch to the correct activity editor
    window.
    """
    App().clean_frame()
    from .edu_windows.edu_module_editor import ModuleEditor
    from .edu_windows.edu_quiz_editor import QuizEditor
    from .edu_windows.edu_challenge_editor import ChallengeEditor

    match option:
        case 'Module':
            App().change_frame(ModuleEditor(existing_activity))
        case 'Quiz':
            App().change_frame(QuizEditor(existing_activity))
        case 'Challenge':
            App().change_frame(ChallengeEditor(existing_activity))
        case _:
            print(f'you spelt {option} wrong :P')


def editor_prompt():
    """
    Function that handles the frame switch to the editor window.
    """
    # from .edu_windows.edu_edit_option import EditorWindow
    from .edu_windows.edu_selection_window import SelectionScreen

    App().clean_frame()
    App().change_frame(SelectionScreen())