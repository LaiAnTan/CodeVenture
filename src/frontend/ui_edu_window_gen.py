from .ui_app import App

def dispatcher(option, existing_activity):
    App().clean_frame()
    from .edu_windows.edu_module_editor import ModuleEditor

    match option:
        case 'Module':
            App().change_frame(ModuleEditor(App(), 800, 650, existing_activity))
        case 'Quiz':
            raise NotImplementedError
        case 'Challange':
            raise NotImplementedError

def editor_prompt():
    from .edu_windows.edu_edit_option import EditorWindow

    App().clean_frame()
    App().change_frame(EditorWindow(App()))