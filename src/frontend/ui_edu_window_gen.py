from .ui_app import App

def dispatcher(option, existing_activity):
    App().clean_frame()
    from .edu_windows.edu_module_editor import ModuleEditor
    from .edu_windows.edu_quiz_editor import QuizEditor
    from .edu_windows.edu_challange_editor import ChallangeEditor

    match option:
        case 'Module':
            App().change_frame(ModuleEditor(existing_activity))
        case 'Quiz':
            App().change_frame(QuizEditor(existing_activity))
        case 'Challange':
            App().change_frame(ChallangeEditor(existing_activity))

def editor_prompt():
    from .edu_windows.edu_edit_option import EditorWindow

    App().clean_frame()
    App().change_frame(EditorWindow())