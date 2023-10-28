from .ui_app import App


def dispatcher(option, existing_activity):
    """
    Function that handles the frame switch to the correct activity editor
    window.
    """
    App().clean_frame()
    from .edu_windows.edu_module_editor import ModuleEditor

    match option:
        case 'Module':
            App().change_frame(ModuleEditor(800, 650, existing_activity))
        case 'Quiz':
            raise NotImplementedError
        case 'Challange':
            raise NotImplementedError


def editor_prompt():
    """
    Function that handles the frame switch to the editor window.
    """
    from .edu_windows.edu_edit_option import EditorWindow

    App().clean_frame()
    App().change_frame(EditorWindow())