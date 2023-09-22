import customtkinter as ctk

from ui_app import App
from ac_quiz import Quiz, Question
from ui_std_window_gen import displayActivitySelections
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

        header_frame = ctk.CTkFrame(self.root.main_frame)
        header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="we",)

        quiz_name = ctk.CTkLabel(
            header_frame,
            text=f"{self.quiz.id} {self.quiz.title}"
        )
        quiz_name.pack(side=ctk.LEFT, padx=5, pady=5)

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda : displayActivitySelections(self.root, self.student),
            width=20
        )
        back_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        ## header details end --------------------------------------------

        content_frame = ctk.CTkFrame(
            self.root.main_frame,
        )
        content_frame.grid(row=1, column=0, padx=5, pady=5)

        ## qna frame ----------------------------

        qna_frame_width = 450
        self.qna_frame = ctk.CTkScrollableFrame(
            content_frame,
            width=qna_frame_width,
            height=460
        )
        self.qna_frame.grid(row=0, column=0, padx=5, pady=5)

        question_block_width = qna_frame_width - 30
        self.generateAllQuestionFrames(question_block_width)
        show_all_questions = self.showAllQuestions()

        ## qna frame end -------------------------------

        ## some optional side bar start -----------------------

        content_frame.rowconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)

        sidebar_width = 150
        button_sidebar_width = 150 - 30
        sidebar_frame = ctk.CTkScrollableFrame(content_frame, width=sidebar_width)
        sidebar_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        check_button = ctk.CTkButton(
            sidebar_frame,
            width=button_sidebar_width,
            text="Check",
            command=lambda : self.checkAnswers(questionStatusFrame, button_sidebar_width)
        )
        check_button.grid(row=0, column=0, padx=5, pady=5)

        show_all_questions = ctk.CTkButton(
            sidebar_frame,
            width=button_sidebar_width,
            text="Show All Questions",
            command= self.showAllQuestions
        )
        show_all_questions.grid(row=1, column=0, padx=5, pady=5)

        questionStatusFrame = ctk.CTkFrame(sidebar_frame, width=sidebar_width)
        questionStatusFrame.grid(row=2, column=0, padx=5, pady=5)

        self.checkAnswers(questionStatusFrame, button_sidebar_width)

        ## some optional side bar end ----------------------------

        ## footer ---------------------------------------------

        footer_frame = ctk.CTkFrame(self.root.main_frame)
        footer_frame.grid(row=2, column=0, padx=5, pady=5)

        submit_button = ctk.CTkButton(
            footer_frame,
            text="Resubmit" if self.alreadydid else "Submit",
            width=150,
            command=self.end
        )
        submit_button.grid(row=0, column=0)

        ## footer end ------------------------------------------

    def generateAllQuestionFrames(self, max_width):
        self.questionFrames : list[ctk.CTkFrame] = []

        for index, questions in enumerate(self.quiz.questions):
            placeholder_frame = QuestionBlock(questions, max_width, self.studentanswer[index], self.qna_frame).generateFrame()
            self.questionFrames.append(placeholder_frame)

    def showAllQuestions(self):
        for widgets in self.qna_frame.winfo_children():
            widgets.grid_forget()

        for index, frames in enumerate(self.questionFrames):
            frames.grid(row=index, column=0, padx=10, pady=10)

    def showOneQuestion(self, index):
        for widgets in self.qna_frame.winfo_children(): 
            widgets.grid_forget()

        self.questionFrames[index].grid(row=0, column=0, padx=10, pady=10)

    def end(self):
        print("Uploading Student's Answer to Database...")
        student_answer = ",".join([str(x.get()) for x in self.studentanswer])
        self.completion_database.updateStudentAnswer(self.student.username, student_answer)
        print("Final Student Answer", student_answer)
        displayActivitySelections(self.root, self.student)

    def checkAnswers(self, questionStatusFrame: ctk.CTkFrame, max_width):
        for widget in questionStatusFrame.winfo_children():
            widget.destroy()

        student_answers = [x.get() for x in self.studentanswer]

        for index, answer in enumerate(student_answers):
            if answer == -1:
                color = "#939393"
                hover_color = "#5A5A5A"
            elif self.quiz.checkAnswers(index, answer):
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
                ## fucking shit piece of shit python doesnt store what was the parameter of the function in lambda
                ## https://stackoverflow.com/questions/31186959/how-to-generate-a-list-of-different-lambda-functions-with-list-comprehension
                ## checks for the value of index AND GEUESS WHAT, INDEX IS DONE TRANSVERSING, ITS GONNA BE 5
                ## need to set the index as default VALUE instead of REFERENCE
                command= lambda index=index: self.showOneQuestion(index)
            )
            statusButton.grid(row=index, column=0, padx=5, pady=5)
        return

if __name__ == "__main__":
    from ui_app import App

    ActivityDictionary()
    main = App()
    QuizWindow(Quiz("QZ0000"), Student("test_student"), main).FillFrames()
    main.main_frame.grid(row=0, column=0)
    main.mainloop()
