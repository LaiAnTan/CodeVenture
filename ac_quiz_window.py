import customtkinter as ctk

from App import App
from ac_quiz import Quiz
from ac_window_gen import selection_screen
from db_ac_completed import ActivityDictionary, QuizCompleted_DB

from user.user_student import Student

class QuizWindow():
    def	__init__(self, quiz: Quiz, student: Student, main_attach: App):
        self.quiz = quiz
        self.user_answer = []
        self.student = student
        self.completion_database: QuizCompleted_DB = ActivityDictionary.getDatabase(self.quiz.id)

        self.alreadydid = self.completion_database.getStudentEntry(self.student.username)
        self.studentanswer = self.processAnswer(self.completion_database.getStudentAnswer(self.student.username))

        self.root = main_attach

    def processAnswer(self, extracted_data: str):
        ret = []
        if extracted_data is None:
            return None
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

        self.user_answer = [None for _ in self.quiz.questions]

        question_block_width = qna_frame_width - 30
        for index, questions in enumerate(self.quiz.questions):
            placeholder_frame = ctk.CTkFrame(
                qna_frame,
                width=question_block_width
            )

            le_prompt = ctk.CTkLabel(
                placeholder_frame,
                text=questions.get_Prompt(),
                width=question_block_width,
                wraplength=question_block_width - 10,
                anchor="w",
                justify="left",
            )

            radio_button_frame = ctk.CTkFrame(
                placeholder_frame,
            )

            self.user_answer[index] = self.studentanswer[index] if self.alreadydid else ctk.IntVar(value=-1)

            for index2, answer in enumerate(questions.get_Options()):
                radio_button = ctk.CTkRadioButton(
                                master=radio_button_frame,
                                text=answer,
                                variable=self.user_answer[index],
                                value=index2,
                                width=question_block_width
                            )
                
                radio_button.grid(
                    row=index2,
                    column=0,
                    pady=2
                )

            le_prompt.grid(
                row=0,
                column=0,
                padx=5,
                pady=5,
            )

            radio_button_frame.grid(
                row=1,
                column=0,
                padx=5,
                pady=5
            )

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
            command= lambda : self.end(self.user_answer)
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
