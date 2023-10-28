import customtkinter as ctk

from ..std_windows.ui_std_activity_window import ActivityWindow
from ..ui_app import App
from ..ui_std_window_gen import displayActivitySelections
from ...backend.user.user_student import Student
from ...backend.activity.ac_classes.ac_quiz import Quiz, Question
from .helper_class.textdisplay import ParagraphDisplayer

from config import LIGHTMODE_GRAY, DARKMODE_GRAY

class QuestionFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, parent_window,
                 question: Question, max_width, 
                 previous_selection: ctk.IntVar,
                 ) -> None:
        super().__init__(master, 
                        fg_color=LIGHTMODE_GRAY if 
                        App().settings.getSettingValue("lightmode").lower() == "true" else
                        DARKMODE_GRAY
                         )

        self.parent = parent_window
        self.question = question
        self.max_width = max_width
        self.previous_selection = previous_selection

        self.prompt = self.question.get_Prompt()

        self.columnconfigure(0, weight=1)

        self.prompt_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.prompt_frame.columnconfigure(0, weight=1)
        self.prompt_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        for index, prompt in enumerate(self.prompt):
            if "IMG-CONT" in prompt:
                self.prompt = self.parent.ImageHandler(
                    prompt.removeprefix('<IMG-CONT>'),
                    200, # TODO: Change this value
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
                self.prompt = ParagraphDisplayer(
                    self.prompt_frame,
                    prompt
                )
            self.prompt.grid(row=index, column=0, sticky='ew')


        self.options_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.options_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

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
    def __init__(self, quiz: Quiz, student: Student):
        super().__init__(quiz, student)
        self.ac: Quiz

        self.stdanswer = self.processAnswer(self.completion_database.getStudentAnswer(self.std.username))
        self.SetFrames()

    def refresh_variables(self):
        self.stdanswer = self.processAnswer(self.completion_database.getStudentAnswer(self.std.username))

    def SetContent(self):
        self.content_frame.rowconfigure(0, weight=1)

        self.content_frame.columnconfigure(0, weight=20)
        self.content_frame.columnconfigure(1, weight=50)
        self.content_frame.columnconfigure(2, weight=10)
        self.content_frame.columnconfigure(3, weight=20)

        pad = ctk.CTkFrame(self.content_frame, fg_color='transparent', width=0, height=0)
        pad.grid(row=0, column=0, padx=5, pady=5, sticky='nswe')

        pad = ctk.CTkFrame(self.content_frame, fg_color='transparent', width=0, height=0)
        pad.grid(row=0, column=3, padx=5, pady=5, sticky='nswe')

        self.InitializeQnAFrame()
        self.SetMainContent()
        self.SetSidebar()

    def InitializeQnAFrame(self):
        self.qna_width = 450
        self.qna_height = 460

        self.qna_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.qna_frame.columnconfigure(0, weight=1)
        self.qna_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.update_idletasks()

    def SetMainContent(self):
        self.question_width = self.qna_width - 30

        self.genAllQuestions()
        self.showAllQuestions()

    def SetSidebar(self):
        sidebar_frame = ctk.CTkScrollableFrame(self.content_frame)
        sidebar_frame.columnconfigure(0, weight=1)
        sidebar_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        check_button = ctk.CTkButton(
            sidebar_frame,
            text="Check",
            command= self.checkAnswers
        )
        check_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        show_all_questions_button = ctk.CTkButton(
            sidebar_frame,
            text="Show All Questions",
            command= self.showAllQuestions
        )
        show_all_questions_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.questionStatusFrame = ctk.CTkFrame(sidebar_frame)
        self.questionStatusFrame.columnconfigure(0, weight=1)
        self.questionStatusFrame.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        self.initAnswersButton()
        self.checkAnswers()

    def SetFooter(self):
        self.footer_frame.columnconfigure(0, weight=1)
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
        for children in self.qna_frame.winfo_children():
            children.grid_forget()
        self.qna_frame._parent_canvas.yview_moveto(0)

    def genAllQuestions(self):
        self.question_frames = []
        for index, questions in enumerate(self.ac.questions):
            q_frame = QuestionFrame(
                self.qna_frame,
                self,
                questions,
                self.question_width,
                self.stdanswer[index]
            )
            self.question_frames.append(q_frame)

    def showAllQuestions(self):
        self.RefreshQnAFrame()
        for index, frame in enumerate(self.question_frames):
            frame.grid(row=index, column=0, padx=5, pady=5, sticky='ew')

    def showOneQuestion(self, index):
        self.RefreshQnAFrame()
        self.question_frames[index].grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    def initAnswersButton(self):
        student_answers = [x.get() for x in self.stdanswer]
        self.statusButtons = []

        for index, answer in enumerate(student_answers):
            statusButton = ctk.CTkButton(
                self.questionStatusFrame,
                text=f"Question {index}",
                command= lambda index=index: self.showOneQuestion(index)
            )
            self.statusButtons.append(statusButton)
            statusButton.grid(row=index, column=0, padx=5, pady=5, sticky='ew')

    def checkAnswers(self):
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

            self.statusButtons[index].configure(
                hover_color=hover_color,
                fg_color=color
            )

    def StudentSubmission(self):
        print("Uploading Student's Answer to backend.database...")
        student_answer = ",".join([str(x.get()) for x in self.stdanswer])
        self.completion_database.updateStudentAnswer(self.std.username, student_answer)
        print("Final Student Answer", student_answer)
        App().go_back_history() 

if __name__ == "__main__":
    from ..ui_app import App
    from ...backend.activity.ac_database.db_ac_completed import ActivityDictionary

    ActivityDictionary()
    App().change_frame(QuizWindow(Quiz("QZ0000"), Student("testsd")))
    App().mainloop()
