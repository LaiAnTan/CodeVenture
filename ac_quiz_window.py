import customtkinter as ctk

from ac_app import App
from ac_quiz import Quiz
from ac_window_gen import selection_screen

class QuizWindow():
    def	__init__(self, quiz: Quiz):
        self.quiz = quiz
        self.user_answer = []
    
    def	FillFrames(self, attach: App):

        ## header details -------------------------------------------

        header_frame = ctk.CTkFrame(
            attach.main_frame
        )

        quiz_name = ctk.CTkLabel(
            header_frame,
            text=f"{self.quiz.id} {self.quiz.title}"
        )

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda : selection_screen(attach),
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
            attach.main_frame,
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

            self.user_answer[index] = ctk.IntVar(value=-1)

            for index2, answer in enumerate(questions.get_Options()):
                radio_button = ctk.CTkRadioButton(
                                master=radio_button_frame,
                                text=answer,
                                command=lambda : self.__beep_boop(self.user_answer),
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
            attach.main_frame,
        )

        submit_button = ctk.CTkButton(
            footer_frame,
            text="Submit",
            width=150,
            command= self.end
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

    def __beep_boop(self, var):
        print("Value has changed = ", [x.get() for x in var])

    def end(self):
        print("imagine it has submitted, HAH, defo implemented this... (fuck)")
        return self.user_answer

