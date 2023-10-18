
import customtkinter as ctk
import os

from ..ui_app import App
from ..ui_app import App
from ..ui_std_window_gen import displayActivitySelections
from .helper_class.ide import IDE
from .helper_class.imagelabel import ImageLabel
from .helper_class.code_runner import CodeRunner
from .ui_std_activity_window import ActivityWindow
from ...backend.activity.ac_classes.ac_challenge import Challange
from ...backend.activity.ac_database.db_ac_completed import ActivityDictionary
from ...backend.user.user_student import Student


class ChallangeWindow(ActivityWindow):

    def __init__(self, challenge: Challange, student: Student, a: App):
        super().__init__(challenge, student, a)
        self.attempted_count = 0
        self.suceeded = False
        self.percentage = 0

        self.codeentry = self.completion_database.getStudentCode(self.std.username)

        self.displayed_frame = None
        self.shittyIDE = None

        self.SetFrames()

    def SetContent(self):
        self.SetMainContent()
        self.SetSidebar()

    def SetMainContent(self):
        content_frame_height = 460
        content_frame_width = 350

        # left side of the frame

        main_content_frame = ctk.CTkFrame(self.content_frame)

        # buttons to switch between 3 frames, question, hint 

        main_content_options_frame = ctk.CTkFrame(
            main_content_frame,
            width=content_frame_width + 20,
            height=95,
        )
        main_content_options_frame.grid(row=0, column=0, padx=5, pady=5)

        question_button = ctk.CTkButton(
            main_content_options_frame,
            width=85,
            height=25,
            text="Question",
            command=lambda: self.QuestionFrames(content_frame_width)
        )
        question_button.grid(row=0, column=0, padx=5, pady=5)

        hint_button = ctk.CTkButton(
            main_content_options_frame,
            width=85,
            height=25,
            text="Hints",
            command=lambda: self.HintFrames(content_frame_width)
        )
        hint_button.grid(row=0, column=1, padx=5, pady=5)

        solution_button = ctk.CTkButton(
            main_content_options_frame,
            width=85,
            height=25,
            text="Solution",
            command=lambda: self.SolutionFrames(content_frame_width)
        )
        solution_button.grid(row=0, column=2, padx=5, pady=5)

        mark_button = ctk.CTkButton(
            main_content_options_frame,
            width=85,
            height=25,
            text="Run Tests",
            command=lambda: self.RunTestCases_GenFrame(content_frame_width)
        )
        mark_button.grid(row=0, column=3, padx=5, pady=5)

        ## main question frame

        self.displayed_frame = ctk.CTkScrollableFrame(
            main_content_frame,
            width=content_frame_width,
            height=content_frame_height - 40
        )

        self.QuestionFrames(content_frame_width)

        self.displayed_frame.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        main_content_frame.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

    def SetSidebar(self):
        sidebar_width = 350
        sidebar_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            width=sidebar_width,
            height=460
        )

        self.shittyIDE = IDE(
            sidebar_frame,
            sidebar_width - 30,
            360,
            self.ac.id.lower(),
            self.std.username,
            self.ac.ModulePath,
            self.codeentry
        )
        self.shittyIDE.grid(row=0, column=0, padx=5, pady=5)

        sidebar_frame.grid(row=0, column=1, padx=5, pady=5)

    def SetFooter(self):
        submit_button = ctk.CTkButton(
            self.footer_frame,
            text="Resubmit" if self.done else "Submit",
            width=150,
            command=lambda: self.StudentSubmission()
        )

        submit_button.grid(row=0, column=0, padx=0, pady=0)

        # footer end ------------------------------------------

    def ImageHandler(self, source, content, max_img_width, attach_frame):
        if source.img.get(content):
            ret_widget = ImageLabel(
                attach_frame,
                f"{source.ModulePath}/{source.img[content]}",
                max_img_width - 50,
            )
        else:
            ret_widget = ctk.CTkLabel(
                attach_frame,
                text=f"Error displaying image {content}",
                width=max_img_width,
                wraplength=max_img_width - 10,
            )
        return ret_widget

    def QuestionFrames(self, frame_width):
        for widget in self.displayed_frame.winfo_children():
            widget.destroy()
        self.displayed_frame.forget()

        for index, content in enumerate(self.ac.content):
            match content[0]:
                case Challange.Content_Type.Paragraph:
                    paragraph = ctk.CTkLabel(
                        self.displayed_frame,
                        text=content[1],
                        width=frame_width - 10,
                        wraplength=frame_width - 20,
                        anchor="w",
                        justify="left"
                    )

                case Challange.Content_Type.Image:
                    paragraph = self.ImageHandler(
                        self.ac,
                        content[1],
                        frame_width,
                        self.displayed_frame
                    )

            paragraph.grid(row=index, column=0, padx=5, pady=5)

    def SolutionFrames(self, frame_width):
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
                        text="ERROR: Attempt More Times to Unlock the Solution!",
                        width=frame_width - 10,
                        wraplength=frame_width - 20,
                        anchor="w",
                        justify="left",
                        text_color="red",
                    )

        solution_widget.grid(row=0, column=0, padx=5, pady=5)

    def HintFrames(self, frame_width):
        for widget in self.displayed_frame.winfo_children():
            widget.destroy()

        for index, content in enumerate(self.ac.hints.content):
            match content[0]:
                case Challange.Content_Type.Paragraph:
                    paragraph = ctk.CTkLabel(
                        self.displayed_frame,
                        text=content[1],
                        width=frame_width - 10,
                        height=10,
                        wraplength=frame_width - 20,
                        anchor="w",
                        justify="left"
                    )

                case Challange.Content_Type.Image:
                    paragraph = self.ImageHandler(
                        self.ac.hints,
                        content[1],
                        frame_width,
                        self.displayed_frame
                    )

            paragraph.grid(row=index, column=0, padx=5, pady=5)

    def RunTestCases(self, test_input):
        own_code = self.shittyIDE.RunTestCases(test_input)
        test_code = CodeRunner(None, None, "solution", self.ac.ModulePath).RunTestCases(f"{self.ac.ModulePath}/{test_input}")
        if own_code == test_code:
            return True, own_code, test_code
        else:
            return False, own_code, test_code

    def RunTestCases_GenFrame(self, frame_width):
        self.attempted_count += 1
        for widget in self.displayed_frame.winfo_children():
            widget.destroy()

        test_cases = os.listdir(f"{self.ac.ModulePath}/testcase")
        cases = len(test_cases)
        correct_cases = 0

        for index, test_case in enumerate(test_cases):
            result, usr_out, sys_out = self.RunTestCases(f"testcase/{test_case}")
            if result == True:
                result = ctk.CTkLabel(
                    self.displayed_frame,
                    text=f"Test {index} -- OK!",
                    text_color="limegreen",
                    font=ctk.CTkFont(
                        "Arial",
                        size=20
                    ),
                    width=frame_width - 10,
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
                        "Arial",
                        size=20
                    ),
                    width=frame_width - 10,
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
                "Arial",
                size=20
            ),
            width=frame_width - 10,
            justify="left",
            anchor="w"
        )
        
        result.grid(row=cases, column=0, padx=5, pady=5)

    def StudentSubmission(self):
        print("Submitting code attempt")
        codecontent = self.shittyIDE.getContents()
        self.completion_database.updateStudentCode(self.std.username, self.percentage, codecontent)
        displayActivitySelections(self.root, self.std)

if __name__ == "__main__":
    from ..ui_app import App

    ActivityDictionary()
    main = App()
    ChallangeWindow(Challange("CH0001"), Student("james"), main).Attach()
    main.main_frame.grid(row=0, column=0)
    main.mainloop()