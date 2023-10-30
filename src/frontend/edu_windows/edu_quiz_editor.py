from __future__ import annotations
import customtkinter as ctk

from ..ui_app import App
from .edu_activity_editor import ActivityEditor
from .helper_class.errorWindow import ErrorWindow
from ...backend.factory.QuizFactory import QuizFactory
from .helper_class.questionPreview import QuestionPreview
from ...backend.activity.ac_classes.ac_quiz import Activity, Quiz
from .helper_class.refreshScrollFrame import RefreshableScrollableFrame


class QuizEditor(ActivityEditor):

    """
    Frame class for displaying the quiz editor window for educators.
    """

    def __init__(self, existing_quiz: Quiz = None):
        """
        Initialises the class.
        """

        super().__init__(Activity.AType['Quiz'], existing_quiz)

        self.asset = []
        self.SetFrames()

    def ContentData(self):
        """
        Add content data into frame.
        """

        self.content_data.rowconfigure(1, weight=1)
        self.content_data.columnconfigure(0, weight=1)

        add_new_question = ctk.CTkButton(
            self.content_data,
            text='Add new Question',
            command=self.addQuestions
        )
        add_new_question.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.para_types = ['Question']

        self.questions = RefreshableScrollableFrame(
            self.content_data
        )
        self.questions.columnconfigure(0, weight=1)
        self.questions.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    def widget_factory(self, not_used):
        """
        Creates question preview and returns it.
        """
        return QuestionPreview(
            self.questions,
            self
        )

    def addQuestions(self):
        """
        Adds a new question into the frame.
        """
        new_question = QuestionPreview(
            self.questions,
            self
        )
        new_question.grid(row=len(self.questions.get_tracking_list()),
                          column=0,
                          sticky='ew')
        self.questions.track_element(new_question)
        self.questions.refresh_elements()
        self.questions.scroll_frame(1)

    def GetContentData(self):
        """
        Creates and returns the content data.
        """
        return [x.getData() for x in self.questions.get_tracking_list()]

    def get_error_list(self):
        """
        Creates and returns the error list.
        """
        error_list = []
        for index, question in enumerate(self.questions.get_tracking_list()):
            error = question.getError()
            if error is not None:
                error_list.append((index + 1, question.getError()))
        return error_list

    def ExportData(self):
        """
        Handles the event where the quiz is exported.
        """
        print("Exporting Quiz....")

        error_list = self.get_error_list()
        content = self.GetContentData()
        if error_list:
            error_window = ErrorWindow(self, 450, 550, error_list,
                                       'exporting quiz activity')
            self.winfo_toplevel().wait_window(error_window)
            return False

        QuizFactory(self.GetHeaderData(), content, self.asset).build()
        print("Exported Quiz!")
        return True


if __name__ == "__main__":
    App().change_frame(QuizEditor())
    App().mainloop()
