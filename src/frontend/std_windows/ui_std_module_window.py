import customtkinter as ctk

from ..ui_app import App
from ...backend.user.user_student import Student
from .ui_std_activity_window import ActivityWindow
from .helper_class.textdisplay import ParagraphDisplayer
from ...backend.activity.ac_classes.ac_module import Module
from ...backend.activity.ac_database.db_ac_completed import ActivityDictionary


class ModuleWindow(ActivityWindow):

    """
    Frame class for displaying the module window.
    """

    def __init__(self, module: Module, student: Student, editor_view=False):
        """
        Initialises the class.
        """

        super().__init__(module, student, editor_view)
        self.SetFrames()

    def SetContent(self):
        """
        Function that performs attachment of content elements onto the main
        frame.
        """

        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=1)
        self.contents = ctk.CTkScrollableFrame(
            self.content_frame,
            width=750
        )
        self.contents.columnconfigure(0, weight=1)
        self.contents.grid(row=0, column=0, padx=5, pady=5, sticky='ns')

        for index, content in enumerate(self.ac.content):
            self.contents.rowconfigure(index, weight=1)
            self.contents.columnconfigure(0, weight=1)
            paragraph_frame = ctk.CTkFrame(self.contents,
                                           fg_color='transparent')
            paragraph_frame.rowconfigure(0, weight=1)
            paragraph_frame.columnconfigure(0, weight=1)
            paragraph_frame.grid(row=index, column=0, padx=5, pady=(0, 5),
                                 sticky='ew')

            match content[0]:
                case Module.Content_Type.Paragraph:
                    paragraph = ParagraphDisplayer(
                        paragraph_frame,
                        content[1]
                    )
                case Module.Content_Type.Image:
                    paragraph = self.ImageHandler(
                        content[1],
                        1600, # TODO: Change the Height Value
                        750,
                        paragraph_frame
                    )
                case Module.Content_Type.Code:
                    paragraph = self.CodeHandler(
                        content[1],
                        750,
                        paragraph_frame
                    )
            paragraph.grid(row=0, column=0, sticky='ew')
            paragraph.update_idletasks()

    def SetFooter(self):
        """
        Function that performs attachment of footer frame elements onto the
        main frame.
        """

        self.footer_frame.columnconfigure(0, weight=1)

        submit_button = ctk.CTkButton(
            self.footer_frame,
            text="Complete",
            width=150,
            command=self.StudentCompletion,
            state="disabled" if self.done else "normal"
        )
        submit_button.grid(row=0, column=0)

    # helper functions

    def StudentCompletion(self):
        """
        Function that handles the completion event of a student when the button
        is pressed.
        """
        print("Adding Student Entry into backend.database...")
        self.completion_database.addStudentEntry((self.std.username,))
        App().go_back_history()


if __name__ == "__main__":
    ActivityDictionary()
    App().change_frame(ModuleWindow(Module("MD0000"), Student("test_student")))
    App().mainloop()
