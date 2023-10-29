
import customtkinter as ctk
import os

from ..ui_app import App
from .helper_class.ide import IDE
from .helper_class.code_runner import CodeRunner
from .ui_std_activity_window import ActivityWindow
from ...backend.activity.ac_classes.ac_challenge import Challange
from ...backend.activity.ac_database.db_ac_completed import ActivityDictionary
from ...backend.user.user_student import Student
from .helper_class.textdisplay import ParagraphDisplayer


class ChallangeWindow(ActivityWindow):

    """
    Frame class for displaying the challenge window.
    """

    def __init__(self, challenge: Challange, student: Student,
                 editor_view=False):
        """
        Initialize the class.
        """

        super().__init__(challenge, student, editor_view)
        self.attempted_count = 0
        self.suceeded = False
        self.percentage = 0

        if not self.editor_view:
            self.codeentry = self.completion_database.getStudentCode(self.std.getUsername())
        else:
            self.codeentry = None

        self.displayed_frame = None
        self.shittyIDE = None

        self.SetFrames()

    def refresh_variables(self):
        """
        Function that resets the variables to default values.
        """
        super().refresh_variables()

        if not self.editor_view:
            self.codeentry = self.completion_database.getStudentCode(self.std.getUsername())

    def SetContent(self):
        """
        Function that handles the setting of contents.
        """

        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=35)
        self.content_frame.columnconfigure(1, weight=65)

        self.SetMainContent()
        self.SetSidebar()

    def SetMainContent(self):
        """
        Function that performs attachment of main frame elements onto the main
        frame.
        """

        content_frame_width = 350

        # left side of the frame

        main_content_frame = ctk.CTkFrame(self.content_frame)
        main_content_frame.rowconfigure(1, weight=1)
        main_content_frame.columnconfigure(0, weight=1)
        main_content_frame.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky='nsew'
        )

        # buttons to switch between 3 frames, question, hint

        main_content_options_frame = ctk.CTkFrame(
            main_content_frame,
        )
        main_content_options_frame.rowconfigure(0, weight=1)
        main_content_options_frame.columnconfigure((0, 1, 2, 3), weight=1)
        main_content_options_frame.grid(row=0, column=0, padx=5, pady=5, sticky='new')

        question_button = ctk.CTkButton(
            main_content_options_frame,
            text="Question",
            width=0,
            command=lambda: self.QuestionFrames(content_frame_width)
        )
        question_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        hint_button = ctk.CTkButton(
            main_content_options_frame,
            text="Hints",
            width=0,
            command=lambda: self.HintFrames(content_frame_width)
        )
        hint_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        solution_button = ctk.CTkButton(
            main_content_options_frame,
            text="Solution",
            width=0,
            command=lambda: self.SolutionFrames(content_frame_width)
        )
        solution_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        mark_button = ctk.CTkButton(
            main_content_options_frame,
            text="Run Tests",
            width=0,
            command=lambda: self.RunTestCases_GenFrame(content_frame_width)
        )
        mark_button.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        # main question frame

        self.displayed_frame = ctk.CTkScrollableFrame(main_content_frame)
        self.displayed_frame.columnconfigure(0, weight=1)
        self.displayed_frame.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky='nswe'
        )

        self.QuestionFrames(content_frame_width)

    def SetSidebar(self):
        """
        Function that performs attachment of sidebar frame elements onto the
        main frame.
        """

        sidebar_frame = ctk.CTkScrollableFrame(
            self.content_frame,
        )
        sidebar_frame.rowconfigure(0, weight=1)
        sidebar_frame.columnconfigure(0, weight=1)
        sidebar_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')

        self.shittyIDE = IDE(
            sidebar_frame,
            450,
            250,
            self.ac.id.lower(),
            self.ac.id,
            self.ac.ModulePath,
            self.codeentry
        )
        self.shittyIDE.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

    def SetFooter(self):
        """
        Function that performs attachment of footer frame elements onto the
        main frame.
        """

        self.footer_frame.columnconfigure(0, weight=1)
        submit_button = ctk.CTkButton(
            self.footer_frame,
            text="Resubmit" if self.done else "Submit",
            width=150,
            command=lambda: self.StudentSubmission()
        )

        submit_button.grid(row=0, column=0, padx=0, pady=0)

    def QuestionFrames(self, frame_width):
        """
        Function that performs attachment of question frame elements.
        """
        for widget in self.displayed_frame.winfo_children():
            widget.destroy()
        self.displayed_frame.forget()

        for index, content in enumerate(self.ac.content):
            match content[0]:
                case Challange.Content_Type.Paragraph:
                    paragraph = ParagraphDisplayer(
                        self.displayed_frame,
                        content[1]
                    )
                case Challange.Content_Type.Image:
                    paragraph = self.ImageHandler(
                        content[1],
                        1600, # change height value later
                        frame_width,
                        self.displayed_frame
                    )
                case Challange.Content_Type.Code:
                    paragraph = self.CodeHandler(
                        content[1],
                        frame_width,
                        self.displayed_frame
                    )
            paragraph.grid(row=index, column=0, sticky='ew')

    def SolutionFrames(self, frame_width):
        """
        Function that performs attachment of solution frame elements.
        """
        for widget in self.displayed_frame.winfo_children():
            widget.destroy()
        self.displayed_frame.forget()

        if self.attempted_count > 5 or self.suceeded:
            solution_widget = CodeRunner(
                self.displayed_frame,
                frame_width - 30,
                "solution",
                self.ac.ModulePath
            )
        else:
            solution_widget = ctk.CTkLabel(
                        self.displayed_frame,
                        text="ERROR: Attempt More Times to Unlock Solution",
                        anchor="w",
                        justify="left",
                        text_color="red",
                    )

        solution_widget.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    def HintFrames(self, frame_width):
        """
        Function that performs attachment of hint frame elements.
        """
        for widget in self.displayed_frame.winfo_children():
            widget.destroy()

        for index, content in enumerate(self.ac.hints.content):
            match content[0]:
                case Challange.Content_Type.Paragraph:
                    paragraph = ParagraphDisplayer(
                        self.displayed_frame,
                        content[1]
                    )
                case Challange.Content_Type.Image:
                    paragraph = self.ImageHandler(
                        content[1],
                        1600,  # TODO: Change the height value
                        frame_width,
                        self.displayed_frame,
                        self.ac.hints
                    )

            paragraph.grid(row=index, column=0, sticky='ew')

    def RunTestCases(self, test_input):
        """
        Function that runs all the test cases.
        """
        own_code = self.shittyIDE.RunTestCases(test_input)
        test_code = CodeRunner(None, None, "solution",
                               self.ac.ModulePath).RunTestCases(f"{self.ac.ModulePath}/{test_input}")
        if own_code == test_code:
            return True, own_code, test_code
        else:
            return False, own_code, test_code

    def RunTestCases_GenFrame(self, frame_width):
        """
        Function that displays the result of all test cases onto a frame.
        """
        self.attempted_count += 1
        for widget in self.displayed_frame.winfo_children():
            widget.destroy()

        test_cases = os.listdir(f"{self.ac.ModulePath}/testcase")
        cases = len(test_cases)
        correct_cases = 0

        for index, test_case in enumerate(test_cases):
            result, o, t = self.RunTestCases(f"testcase/{test_case}")
            if result is True:
                result = ctk.CTkLabel(
                    self.displayed_frame,
                    text=f"Test {index} -- OK!",
                    text_color="limegreen",
                    font=ctk.CTkFont(
                        "Helvetica",
                        size=20
                    ),
                    justify="left",
                    anchor="w"
                )
                correct_cases += 1
            else:
                result = ctk.CTkLabel(
                    self.displayed_frame,
                    text=f"Test {index} -- KO!",
                    text_color="red",
                    font=ctk.CTkFont(
                        "Helvetica",
                        size=20
                    ),
                    justify="left",
                    anchor="w"
                )

            result.grid(row=index, column=0, padx=5, pady=5)

        self.suceeded = (correct_cases == cases)
        self.percentage = correct_cases / cases

        result = ctk.CTkLabel(
            self.displayed_frame,
            text=f"Test {correct_cases}/{cases} passed!",
            text_color="yellow",
            font=ctk.CTkFont(
                "Helvetica",
                size=20
            ),
            justify="left",
            anchor="w"
        )

        result.grid(row=cases, column=0, padx=5, pady=5)

    def StudentSubmission(self):
        """
        Function that handles the submission event when button is pressed.
        """
        print("Submitting code attempt")
        codecontent = self.shittyIDE.getCodeContent()
        self.completion_database.updateStudentCode(self.std.username,
                                                   self.percentage,
                                                   codecontent)
        App().go_back_history()


if __name__ == "__main__":
    ActivityDictionary()
    App().change_frame(ChallangeWindow(Challange("CH0001"), Student("james")))
    App().mainloop()
