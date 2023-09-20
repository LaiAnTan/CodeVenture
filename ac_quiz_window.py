import customtkinter as ctk

from App import App
from ac_quiz import Quiz, Question
from ac_window_gen import selection_screen
from db_ac_completed import ActivityDictionary, QuizCompleted_DB

from user.user_student import Student

class QuestionBlock():
    def __init__(self, question: Question, max_width, previous_selection, attach_to) -> None:
        self.question = question
        self.max_width = max_width
        self.previous_selection = previous_selection
        self.frame = attach_to

    def generateFrame(self):
        return_frame = ctk.CTkFrame(self.frame)

        le_prompt = ctk.CTkLabel(
            return_frame,
            text=self.question.get_Prompt(),
            width=self.max_width,
            wraplength=self.max_width - 10,
            anchor="w",
            justify="left",
        )
        le_prompt.grid(row=0, column=0, padx=5, pady=5)

        radio_button_frame = ctk.CTkFrame(return_frame)
        radio_button_frame.grid(row=1, column=0, padx=5, pady=5)

        for index2, answer in enumerate(self.question.get_Options()):
            radio_button = ctk.CTkRadioButton(
                            master=radio_button_frame,
                            text=answer,
                            variable=self.previous_selection,
                            value=index2,
                            width=self.max_width
                        )
            radio_button.grid(row=index2, column=0, pady=2)

        return return_frame

class QuizWindow():
    def	__init__(self, quiz: Quiz, student: Student, main_attach: App):
        self.quiz = quiz
        self.student = student
        self.completion_database: QuizCompleted_DB = ActivityDictionary.getDatabase(self.quiz.id)

        self.alreadydid = self.completion_database.getStudentEntry(self.student.username)
        self.studentanswer = self.processAnswer(self.completion_database.getStudentAnswer(self.student.username))

        self.root = main_attach

    def processAnswer(self, extracted_data: str):
        ret = []
        if extracted_data is None:
            return [ctk.IntVar(value=-1) for _ in self.quiz.questions]
        for answer in extracted_data.split(','):
            ret.append(ctk.IntVar(value=(int(answer))))
        return ret

    def	FillFrames(self):

        ## header details -------------------------------------------

        header_frame = ctk.CTkFrame(
            self.root.main_frame
        )

        quiz_name = ctk.CTkLabel(
            header_frame,
            text=f"{self.quiz.id} {self.quiz.title}"
        )

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda : selection_screen(self.root, self.student),
            width=20
        )

        quiz_name.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5
        )

        ## this garbage dont wanna go to the right
        ## SO EVERYONE NEEDS PACK NOW WOWW

        back_button.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )

        header_frame.grid(
            row=0,
            column=0,
            sticky="we",
            padx=5,
            pady=5
        )

        ## header details end --------------------------------------------

        content_frame = ctk.CTkFrame(
            self.root.main_frame,
        )

        ## qna frame ----------------------------

        qna_frame_width = 450
        qna_frame = ctk.CTkScrollableFrame(
            content_frame,
            width=qna_frame_width,
            height=460
        )

        question_block_width = qna_frame_width - 30
        for index, questions in enumerate(self.quiz.questions):
            placeholder_frame = QuestionBlock(questions, question_block_width, self.studentanswer[index], qna_frame).generateFrame()

            placeholder_frame.grid(
                row=index,
                column=0,
                padx=10,
                pady=10
            )
        
        qna_frame.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        ## qna frame end -------------------------------

        ## some optional side bar start -----------------------

        sidebar_width = 150
        sidebar_frame = ctk.CTkFrame(
            content_frame,
            width=sidebar_width
        )

        content_frame.rowconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)

        some_label = ctk.CTkLabel(
            sidebar_frame,
            text="Insert Some Revelant Text here, or some hyperlinks, idk go wild",
            width=sidebar_width,
            wraplength=sidebar_width,
        )

        some_label2 = ctk.CTkLabel(
            sidebar_frame,
            text="haha stinky poopy stinky stinky amongus sus",
            width=sidebar_width,
            wraplength=sidebar_width
        )

        some_label.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        some_label2.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        sidebar_frame.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="ns"
        )
        
        ## some optional side bar end ----------------------------
        
        content_frame.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
        )

        ## footer ---------------------------------------------

        footer_frame = ctk.CTkFrame(
            self.root.main_frame,
        )

        submit_button = ctk.CTkButton(
            footer_frame,
            text="Resubmit" if self.alreadydid else "Submit",
            width=150,
            command= lambda : self.end(self.studentanswer)
        )

        submit_button.grid(
            row=0,
            column=0,
            padx=0,
            pady=0
        )

        footer_frame.grid(
            row=2,
            column=0,
            padx=5,
            pady=5
        )

        ## footer end ------------------------------------------

    def end(self, tk_input):
        print("Uploading Student's Answer to Database...")
        student_answer = ",".join([str(x.get()) for x in tk_input])
        self.completion_database.updateStudentAnswer(self.student.username, student_answer)
        print("Final Student Answer", student_answer)
        selection_screen(self.root, self.student)

if __name__ == "__main__":
    from App import App

    ActivityDictionary()
    main = App()
    QuizWindow(Quiz("QZ0000"), Student("test_student"), main).FillFrames()
    main.main_frame.grid(row=0, column=0)
    main.mainloop()
