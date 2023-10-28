import customtkinter as ctk

from ..ui_app import App
from ...backend.user.user_student import Student
from ..std_windows.ui_std_activity_window import ActivityWindow
from ...backend.activity.ac_classes.ac_quiz import Quiz, Question


class QuestionFrame(ctk.CTkFrame):

    """
    Frame class for displaying a question.
    """

    def __init__(self, master: ctk.CTkFrame, parent_window,
                 question: Question, max_width,
                 previous_selection: ctk.IntVar,
                 ) -> None:
        """
        Initialises the class.
        """
        super().__init__(master)

        self.parent = parent_window
        self.question = question
        self.max_width = max_width
        self.previous_selection = previous_selection

        self.prompt = self.question.get_Prompt()

        self.prompt_frame = ctk.CTkFrame(self)
        self.prompt_frame.grid(row=0, column=0, padx=5, pady=5)

        for index, prompt in enumerate(self.prompt):
            if "IMG-CONT" in prompt:
                self.prompt = self.parent.ImageHandler(
                    prompt.removeprefix('<IMG-CONT>'),
                    200,  # TODO: Change this value
                    self.max_width,
                    self.prompt_frame
                )
            elif "CODE-CONT" in prompt:
                self.prompt = self.parent.CodeHandler(
                    prompt.removeprefix('<CODE-CONT>'),
                    self.max_width,
                    self.prompt_frame
                )
            else:
                self.prompt = ctk.CTkLabel(
                    self.prompt_frame,
                    text=prompt,
                    width=self.max_width,
                    wraplength=self.max_width - 10,
                    anchor="w",
                    justify="left",
                )
            self.prompt.grid(row=index, column=0, padx=5, pady=5)

        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=1, column=0, padx=5, pady=5)

        for index, answer in enumerate(self.question.get_Options()):
            option = ctk.CTkRadioButton(
                        master=self.options_frame,
                        text=answer,
                        variable=self.previous_selection,
                        value=index,
                        width=self.max_width
                    )
            option.grid(row=index, column=0, pady=2, padx=5)


class QuizWindow(ActivityWindow):

    """
    Frame class for displaying the quiz window.
    """

    def __init__(self, quiz: Quiz, student: Student):
        super().__init__(quiz, student)
        self.ac: Quiz

        self.stdanswer = self.processAnswer(self.completion_database
                                            .getStudentAnswer(self.std
                                                              .getUsername()))
        self.SetFrames()

    def refresh_variables(self):
        """
        Function that resets the variables to default values.
        """
        self.stdanswer = self.processAnswer(self.completion_database
                                            .getStudentAnswer(self.std
                                                              .getUsername()))

    def InitializeQnAFrame(self):
        """
        Function that initialises the QnA Frame.
        """
        self.qna_width = 450
        self.qna_height = 460

        self.qna_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            width=self.qna_width,
            height=self.qna_height
        )
        self.qna_frame.grid(row=0, column=0, padx=5, pady=5)

    def SetContent(self):
        """
        Function that handles the init & setting of contents.
        """
        self.InitializeQnAFrame()
        self.SetMainContent()
        self.SetSidebar()

    def SetMainContent(self):
        """
        Function that handles the setting of the main content (questions).
        """
        self.question_width = self.qna_width - 30
        self.showAllQuestions()

    def SetSidebar(self):
        """
        Function that handles the attachment of the sidebar to the main frame.
        """
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)

        sidebar_width = 150
        button_sidebar_width = sidebar_width - 30
        sidebar_frame = ctk.CTkScrollableFrame(self.content_frame,
                                               width=sidebar_width)
        sidebar_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        check_button = ctk.CTkButton(
            sidebar_frame,
            width=button_sidebar_width,
            text="Check",
            command=lambda: self.checkAnswers(questionStatusFrame,
                                              button_sidebar_width)
        )
        check_button.grid(row=0, column=0, padx=5, pady=5)

        show_all_questions_button = ctk.CTkButton(
            sidebar_frame,
            width=button_sidebar_width,
            text="Show All Questions",
            command=self.showAllQuestions
        )
        show_all_questions_button.grid(row=1, column=0, padx=5, pady=5)

        questionStatusFrame = ctk.CTkFrame(sidebar_frame, width=sidebar_width)
        questionStatusFrame.grid(row=2, column=0, padx=5, pady=5)

        self.checkAnswers(questionStatusFrame, button_sidebar_width)

    def SetFooter(self):
        """
        Function that handles the attachment of footer elements to the
        main frame.
        """
        submit_button = ctk.CTkButton(
            self.footer_frame,
            text="Resubmit" if self.done else "Submit",
            width=150,
            command=self.StudentSubmission
        )
        submit_button.grid(row=0, column=0)

    # helper functions

    def processAnswer(self, extracted_data: str):
        """
        Function that parses the answer into a list when extracted_data is
        inputted.
        """
        ret = []
        if extracted_data is None:
            return [ctk.IntVar(value=-1) for _ in self.ac.questions]
        for answer in extracted_data.split(','):
            ret.append(ctk.IntVar(value=(int(answer))))
        return ret

    def RefreshQnAFrame(self):
        """
        Function that refreshes the QnA frame.
        """
        self.qna_frame.destroy()
        self.qna_frame = ctk.CTkScrollableFrame(self.content_frame,
                                                width=self.qna_width,
                                                height=self.qna_height)
        self.qna_frame.grid(row=0, column=0, padx=5, pady=5)

    def showAllQuestions(self):
        """
        Function that handles the attachment of  all questions onto
        the main frame.
        """
        self.RefreshQnAFrame()
        for index, questions in enumerate(self.ac.questions):
            q_frame = QuestionFrame(
                self.qna_frame,
                self,
                questions,
                self.question_width,
                self.stdanswer[index]
            )
            q_frame.grid(row=index, column=0, padx=5, pady=5)

    def showOneQuestion(self, index):
        """
        Function that attaches a singular question onto the main frame.
        """
        self.RefreshQnAFrame()
        q_frame = QuestionFrame(
            self.qna_frame,
            self,
            self.ac.questions[index],
            self.question_width,
            self.stdanswer[index]
        )
        q_frame.grid(row=0, column=0, padx=5, pady=5)

    def checkAnswers(self, questionStatusFrame: ctk.CTkFrame, max_width):
        """
        Function that checks the student's answers with the correct answers,
        and displays the appropriate status.
        """
        for widget in questionStatusFrame.winfo_children():
            widget.destroy()

        student_answers = [x.get() for x in self.stdanswer]

        for index, answer in enumerate(student_answers):
            if answer == -1:
                color = "#939393"
                hover_color = "#5A5A5A"
            elif self.ac.checkAnswers(index, answer):
                color = "#40C025"
                hover_color = "#2E9618"
            else:
                color = "#BB351E"
                hover_color = "#962B18"

            statusButton = ctk.CTkButton(
                questionStatusFrame,
                text=f"Question {index}",
                hover_color=hover_color,
                fg_color=color,
                width=max_width,
                command=lambda index=index: self.showOneQuestion(index)
            )
            statusButton.grid(row=index, column=0, padx=5, pady=5)

    def StudentSubmission(self):
        """
        Function that handles the submission event when a student presses the
        submit button.
        """
        print("Uploading Student's Answer to backend.database...")
        student_answer = ",".join([str(x.get()) for x in self.stdanswer])
        self.completion_database.updateStudentAnswer(self.std.username,
                                                     student_answer)
        print("Final Student Answer", student_answer)
        App().go_back_history()


if __name__ == "__main__":
    from ...backend.activity.ac_database.db_ac_completed import \
        ActivityDictionary

    ActivityDictionary()
    main = App()
    q_frame = QuizWindow(Quiz("QZ0000"), Student("test_student"), main)
    q_frame.grid(row=0, column=0, padx=5, pady=5)
    main.main_frame.grid(row=0, column=0)
    main.mainloop()
