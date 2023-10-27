import customtkinter as ctk

from ..ui_app import App
from .edu_activity_editor import ActivityEditor
from ...backend.activity.ac_classes.ac_quiz import Activity, Quiz

class QuizEditor(ActivityEditor):
    def __init__(self, existing_quiz: Quiz = None):
        super().__init__(Activity.AType['Quiz'], existing_quiz)

        self.asset = []
        self.SetFrames()

    def ContentData(self):
        pass

    def GetContentData(self):
        pass

    def ExportData(self):
        print("Exporting Quiz....")

        print("Exported Quiz!")

if __name__ == "__main__":
    App().change_frame(QuizEditor())
    App().mainloop()