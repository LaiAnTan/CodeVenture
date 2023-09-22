import customtkinter as ctk
import os

from ui_app import App
from ac_challenge import Challange
from ui_std_window_gen import displayActivitySelections

from ac_ide import IDE

from ac_imagelabel import ImageLabelGen

from ac_code_runner import CodeRunner

from db_ac_completed import ActivityDictionary, ChallangeCompleted_DB

from user.user_student import Student

class ChallangeWindow():
    def __init__(self, challenge: Challange, student: Student, a: App):
        self.attempted_count = 0
        self.suceeded = False
        self.percentage = 0
        self.challenge = challenge
        self.student = student
        self.root = a

        self.completion_database: ChallangeCompleted_DB = ActivityDictionary.getDatabase(self.challenge.id)

        self.alreadydid = self.completion_database.getStudentEntry(self.student.username)
        self.codeentry = self.completion_database.getStudentCode(self.student.username)

        self.main_showcontent_frame = None
        self.shittyIDE = None

        self.student = student

    def ImageHandler(self, source, content, max_img_width, attach_frame):
        if source.img.get(content):
            ret_widget = ImageLabelGen(
                f"{source.ModulePath}/{source.img[content]}",
                max_img_width - 50,
                attach_frame
            ).ImageLabelGen()
        else:
            ret_widget = ctk.CTkLabel(
                attach_frame,
                text=f"Error displaying image {content}",
                width=max_img_width,
                wraplength=max_img_width - 10,
            )
        return ret_widget

    def QuestionFrames(self, frame_width):
        for widget in self.main_showcontent_frame.winfo_children():
            widget.destroy()
        self.main_showcontent_frame.forget()

        for index, content in enumerate(self.challenge.content):
            paragraph_frame = ctk.CTkFrame(
                self.main_showcontent_frame
            )

            match content[0]:
                case Challange.Content_Type.Paragraph:
                    paragraph = ctk.CTkLabel(
                        paragraph_frame,
                        text=content[1],
                        width=frame_width - 10,
                        wraplength=frame_width - 20,
                        anchor="w",
                        justify="left"
                    )

                case Challange.Content_Type.Image:
                    paragraph = self.ImageHandler(
                        self.challenge,
                        content[1],
                        frame_width,
                        paragraph_frame
                    )
            
            paragraph.grid(row=0, column=0, padx=5, pady=5)
            paragraph_frame.grid(row=index, column=0, pady=5)

    def	SolutionFrames(self, frame_width):
        for widget in self.main_showcontent_frame.winfo_children():
            widget.destroy()
        self.main_showcontent_frame.forget()

        if self.attempted_count > 5 or self.suceeded:
            solution_widget = CodeRunner(
                frame_width - 30,
                self.main_showcontent_frame,
                "solution",
                self.challenge.ModulePath
            ).setUpFrame()
        else:
            solution_widget = ctk.CTkLabel(
                        self.main_showcontent_frame,
                        text="ERROR: Attempt More Times to Unlock the Solution!",
                        width=frame_width - 10,
                        wraplength=frame_width - 20,
                        anchor="w",
                        justify="left",
                        text_color="red",
                    )

        solution_widget.grid(row=0, column=0, padx=5, pady=5)

    def HintFrames(self, frame_width):
        for widget in self.main_showcontent_frame.winfo_children():
            widget.destroy()

        for index, content in enumerate(self.challenge.hints.content):
            paragraph_frame = ctk.CTkFrame(
                self.main_showcontent_frame
            )

            match content[0]:
                case Challange.Content_Type.Paragraph:
                    paragraph = ctk.CTkLabel(
                        paragraph_frame,
                        text=content[1],
                        width=frame_width - 10,
                        height=10,
                        wraplength=frame_width - 20,
                        anchor="w",
                        justify="left"
                    )

                case Challange.Content_Type.Image:
                    paragraph = self.ImageHandler(
                        self.challenge.hints,
                        content[1],
                        frame_width,
                        paragraph_frame
                    )
            
            paragraph.grid(row=0, column=0,)
            paragraph_frame.grid(row=index, column=0, pady=5)

    def RunTestCases(self, test_input):
        own_code = self.shittyIDE.RunTestCases(test_input)
        test_code = CodeRunner(None, None, "solution", self.challenge.ModulePath).RunTestCases(f"{self.challenge.ModulePath}/{test_input}")
        if own_code == test_code:
            return True, own_code, test_code
        else:
            return False, own_code, test_code

    def RunTestCases_GenFrame(self, frame_width):
        self.attempted_count += 1
        for widget in self.main_showcontent_frame.winfo_children():
            widget.destroy()

        test_cases = os.listdir(f"{self.challenge.ModulePath}/testcase")
        cases = len(test_cases)
        correct_cases = 0

        for index, test_case in enumerate(test_cases):
            result, usr_out, sys_out = self.RunTestCases(f"testcase/{test_case}")
            if result == True:
                result = ctk.CTkLabel(
                    self.main_showcontent_frame,
                    text=f"Test {index} -- OK!",
                    text_color="limegreen",
                    font=ctk.CTkFont(
                        "Noto Sans Mono",
                        size=20
                    ),
                    width=frame_width - 10,
                    justify="left",
                    anchor="w"
                )
                correct_cases += 1
            else:
                result = ctk.CTkLabel(
                    self.main_showcontent_frame,
                    text=f"Test {index} -- KO!",
                    text_color="red",
                    font=ctk.CTkFont(
                        "Noto Sans Mono",
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
            self.main_showcontent_frame,
            text=f"Test {correct_cases}/{cases} passed!",
            text_color="yellow",
            font=ctk.CTkFont(
                "Noto Sans Mono",
                size=20
            ),
            width=frame_width - 10,
            justify="left",
            anchor="w"
        )
        
        result.grid(row=cases, column=0, padx=5, pady=5)

    def	FillFrames(self):
        ## header details -------------------------------------------

        header_frame = ctk.CTkFrame(self.root.main_frame)

        challange_name = ctk.CTkLabel(
            header_frame,
            text=f"{self.challenge.id} {self.challenge.title}"
        )

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda : displayActivitySelections(self.root, self.student),
            width=20
        )

        challange_name.pack(side=ctk.LEFT, padx=5, pady=5)
        back_button.pack(side=ctk.RIGHT, padx=5, pady=5)
        header_frame.grid(row=0, column=0, sticky="we", padx=5, pady=5)

        ## header details end --------------------------------------------

        content_frame = ctk.CTkFrame(self.root.main_frame)

        content_frame_height = 460
        content_frame_width = 350

        ## left side of the frame

        main_content_frame = ctk.CTkFrame(content_frame)

        ## buttons to switch between 3 frames, question, hint 

        main_content_options_frame = ctk.CTkFrame(
            main_content_frame,
            width=content_frame_width + 20,
            height=95,
        )

        question_button = ctk.CTkButton(
            main_content_options_frame,
            width=85,
            height=25,
            text="Question",
            command=lambda : self.QuestionFrames(content_frame_width)
        )

        hint_button = ctk.CTkButton(
            main_content_options_frame,
            width=85,
            height=25,
            text="Hints",
            command=lambda : self.HintFrames(content_frame_width)
        )

        solution_button = ctk.CTkButton(
            main_content_options_frame,
            width=85,
            height=25,
            text="Solution",
            command=lambda : self.SolutionFrames(content_frame_width)
        )

        mark_button = ctk.CTkButton(
            main_content_options_frame,
            width=85,
            height=25,
            text="Run Tests",
            command=lambda : self.RunTestCases_GenFrame(content_frame_width)
        )

        question_button.grid(row=0, column=0, padx=5, pady=5)
        hint_button.grid(row=0, column=1, padx=5, pady=5)
        solution_button.grid(row=0, column=2, padx=5, pady=5)
        mark_button.grid(row=0, column=3, padx=5, pady=5)

        main_content_options_frame.grid(row=0, column=0, padx=5, pady=5)

        ## main question frame

        self.main_showcontent_frame = ctk.CTkScrollableFrame(
            main_content_frame,
            width=content_frame_width,
            height=content_frame_height - 40
        )

        self.QuestionFrames(content_frame_width)

        self.main_showcontent_frame.grid(
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

        ## left side of the frame done

        ## some optional side bar start -----------------------

        sidebar_width = 350
        sidebar_frame = ctk.CTkScrollableFrame(
            content_frame,
            width=sidebar_width,
            height=460
        )

        self.shittyIDE = IDE(
            sidebar_width,
            sidebar_frame,
            self.challenge.id.lower(),
            "ST000", ## will change later
            self.challenge.ModulePath
        )

        a_shitty_ide_frame = self.shittyIDE.setUpFrame(self.codeentry)

        a_shitty_ide_frame.grid(row=0, column=0, padx=5, pady=5)
        sidebar_frame.grid(row=0, column=1, padx=5, pady=5)
        
        ## some optional side bar end ----------------------------

        content_frame.grid(row=1, column=0, padx=5, pady=5,)

        ## footer ---------------------------------------------

        footer_frame = ctk.CTkFrame(
            self.root.main_frame,
        )

        submit_button = ctk.CTkButton(
            footer_frame,
            text="Resubmit" if self.alreadydid else "Submit",
            width=150,
            command= lambda : self.end(self.shittyIDE.getContents())
        )

        submit_button.grid(row=0, column=0, padx=0, pady=0)

        footer_frame.grid(row=2, column=0, padx=5, pady=5)

        ## footer end ------------------------------------------

    def end(self, codecontent):
        print("Submitting code attempt")
        self.completion_database.updateStudentCode(self.student.username, self.percentage, codecontent)
        displayActivitySelections(self.root, self.student)

if __name__ == "__main__":
    from ui_app import App

    ActivityDictionary()
    main = App()
    ChallangeWindow(Challange("CH0001"), Student("test_student"), main).FillFrames()
    main.main_frame.grid(row=0, column=0)
    main.mainloop()