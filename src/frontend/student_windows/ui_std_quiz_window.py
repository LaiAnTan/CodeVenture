import customtkinter as ctk

from ..student_windows.ui_std_activity_window import ActivityWindow
from ..ui_app import App
from ..ui_std_window_gen import displayActivitySelections
from ...backend.user.user_student import Student
from ...backend.activity.ac_classes.ac_quiz import Quiz, Question

class QuestionFrame(ctk.CTkFrame):
    def __init__(self, question: Question, max_width, previous_selection: ctk.IntVar, master: ctk.CTkFrame) -> None:
        super().__init__(master)

        self.question = question
        self.max_width = max_width
        self.previous_selection = previous_selection

        self.prompt_frame = ctk.CTkFrame(self)
        self.prompt_frame.grid(row=0, column=0, padx=5, pady=5)

        self.prompt = ctk.CTkLabel(
            self.prompt_frame,
            text=self.question.get_Prompt(),
            width=self.max_width,
            wraplength=self.max_width - 10,
            anchor="w",
            justify="left",
        )
        self.prompt.grid(row=0, column=0, padx=5, pady=5)

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
    def __init__(self, quiz: Quiz, student: Student, main_attach: App):
        super().__init__(quiz, student, main_attach)
        self.ac: Quiz

        self.stdanswer = self.processAnswer(self.completion_database.getStudentAnswer(self.std.username))
        self.InitializeQnAFrame()
        self.SetFrames()

    def InitializeQnAFrame(self):
        self.qna_width = 450
        self.qna_height = 460

        self.qna_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            width=self.qna_width,
            height=self.qna_height
        )
        self.qna_frame.grid(row=0, column=0, padx=5, pady=5)

    def SetContent(self):
        self.SetMainContent()
        self.SetSidebar()

    def SetMainContent(self):
        self.question_width = self.qna_width - 30
        self.showAllQuestions()

    def SetSidebar(self):
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)

        sidebar_width = 150
        button_sidebar_width = sidebar_width - 30
        sidebar_frame = ctk.CTkScrollableFrame(self.content_frame, width=sidebar_width)
        sidebar_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        check_button = ctk.CTkButton(
            sidebar_frame,
            width=button_sidebar_width,
            text="Check",
            command=lambda : self.checkAnswers(questionStatusFrame, button_sidebar_width)
        )
        check_button.grid(row=0, column=0, padx=5, pady=5)

        show_all_questions_button = ctk.CTkButton(
            sidebar_frame,
            width=button_sidebar_width,
            text="Show All Questions",
            command= self.showAllQuestions
        )
        show_all_questions_button.grid(row=1, column=0, padx=5, pady=5)

        questionStatusFrame = ctk.CTkFrame(sidebar_frame, width=sidebar_width)
        questionStatusFrame.grid(row=2, column=0, padx=5, pady=5)

        self.checkAnswers(questionStatusFrame, button_sidebar_width)

    def SetFooter(self):
        submit_button = ctk.CTkButton(
            self.footer_frame,
            text="Resubmit" if self.done else "Submit",
            width=150,
            command=self.StudentSubmission
        )
        submit_button.grid(row=0, column=0)

    ## helper functions

    def processAnswer(self, extracted_data: str):
        ret = []
        if extracted_data is None:
            return [ctk.IntVar(value=-1) for _ in self.ac.questions]
        for answer in extracted_data.split(','):
            ret.append(ctk.IntVar(value=(int(answer))))
        return ret

    def RefreshQnAFrame(self):
        self.qna_frame.destroy()
        self.qna_frame = ctk.CTkScrollableFrame(self.content_frame, width=self.qna_width, height=self.qna_height)
        self.qna_frame.grid(row=0, column=0, padx=5, pady=5)

    def showAllQuestions(self):
        self.RefreshQnAFrame()
        for index, questions in enumerate(self.ac.questions):
            q_frame = QuestionFrame(questions, self.question_width, self.stdanswer[index], self.qna_frame)
            q_frame.grid(row=index, column=0, padx=5, pady=5)

    def showOneQuestion(self, index):
        self.RefreshQnAFrame()
        q_frame = QuestionFrame(self.ac.questions[index], self.question_width, self.stdanswer[index], self.qna_frame)
        q_frame.grid(row=0, column=0, padx=5, pady=5)

    def checkAnswers(self, questionStatusFrame: ctk.CTkFrame, max_width):
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
                command= lambda index=index: self.showOneQuestion(index)
            )
            statusButton.grid(row=index, column=0, padx=5, pady=5)

    def StudentSubmission(self):
        print("Uploading Student's Answer to backend.database...")
        student_answer = ",".join([str(x.get()) for x in self.stdanswer])
        self.completion_backend.database.updateStudentAnswer(self.std.username, student_answer)
        print("Final Student Answer", student_answer)
        displayActivitySelections(self.root, self.std)

if __name__ == "__main__":
    from ..ui_app import App
    from backend.activity.ac_database.db_ac_completed import ActivityDictionary

    ActivityDictionary()
    main = App()
    q_frame = QuizWindow(Quiz("QZ0000"), Student("test_student"), main)
    q_frame.grid(row=0, column=0, padx=5, pady=5)
    main.main_frame.grid(row=0, column=0)
    main.mainloop()
