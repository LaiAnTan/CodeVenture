import customtkinter as ctk

from App import App
from ac_module import Module
from ac_window_gen import selection_screen
from db_ac_completed import ActivityDictionary

from ac_code_runner import CodeRunner
from ac_imagelabel import ImageLabelGen

from user.user_student import Student

class ModuleWindow():
    def	__init__(self, module: Module, student: Student, main_attach: App):
        self.module = module
        self.student = student
        self.completion_database = ActivityDictionary.getDatabase(self.module.id)
        self.alreadydid = self.completion_database.getStudentEntry(self.student.username) != None
        self.root = main_attach

    def ImageHandler(self, content, max_img_width, attach_to):
        if self.module.img.get(content):
            ret_widget = ImageLabelGen(
                f"{self.module.ModulePath}/{self.module.img[content]}",
                max_img_width - 50,
                attach_to
            ).ImageLabelGen()
        else:
            ret_widget = ctk.CTkLabel(
                attach_to,
                text=f"Error displaying image {content}",
                width=max_img_width,
                wraplength=max_img_width - 10,
            )
        return ret_widget
    
    def CodeHandler(self, content, max_img_width, attach_to):
        if self.module.code.get(content):
            ret_widget = CodeRunner(max_img_width - 30,
                            attach_to,
                            self.module.code[content],
                            self.module.ModulePath
                            ).setUpFrame()
        else:
            ret_widget = ctk.CTkLabel(
                attach_to,
                text=f"Error displaying code {content}",
                width=max_img_width,
                wraplength=max_img_width - 10,
            )
        return ret_widget

    def FillFrames(self):

        ## header details -------------------------------------------

        header_frame = ctk.CTkFrame(self.root.main_frame)

        quiz_name = ctk.CTkLabel(
            header_frame,
            text=f"{self.module.id} {self.module.title}"
        )

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda : selection_screen(self.root, self.student),
            width=20
        )

        quiz_name.pack(side=ctk.LEFT, padx=5, pady=5)
        back_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        header_frame.grid(row=0, column=0, sticky="we", padx=5, pady=5)

        ## header details end --------------------------------------------

        content_frame = ctk.CTkFrame(self.root.main_frame)

        ## main_content frame ----------------------------

        main_content_frame_width = 550

        main_content_frame = ctk.CTkScrollableFrame(
            content_frame,
            width=main_content_frame_width,
            height=460
        )

        paragraph_frame_width = main_content_frame_width - 20

        for index, content in enumerate(self.module.content):
            paragraph_frame = ctk.CTkFrame(
                main_content_frame
            )

            match content[0]:
                case Module.Content_Type.Paragraph:
                    paragraph = ctk.CTkLabel(
                        paragraph_frame,
                        text=content[1],
                        width=paragraph_frame_width,
                        wraplength=paragraph_frame_width - 10,
                        anchor="w",
                        justify="left"
                    )

                case Module.Content_Type.Image:
                    paragraph = self.ImageHandler(
                        content[1],
                        paragraph_frame_width,
                        paragraph_frame
                    )

                case Module.Content_Type.Code:
                    paragraph = self.CodeHandler(
                        content[1],
                        paragraph_frame_width,
                        paragraph_frame
                    )

            paragraph.grid(row=0, column=0, padx=5, pady=5)
            paragraph_frame.grid(row=index, column=0, padx=5, pady=10)

        main_content_frame.grid(row=0, column=0, padx=5, pady=5)

        ## qna frame end -------------------------------

        ## some optional side bar start -----------------------

        sidebar_width = 50
        sidebar_frame = ctk.CTkFrame(
            content_frame,
            width=sidebar_width
        )

        some_label = ctk.CTkLabel(
            sidebar_frame,
            text="does module need a side bar tho....?",
            width=sidebar_width,
            wraplength=sidebar_width,
        )

        some_label.grid(row=0, column=0, padx=5, pady=5)

        sidebar_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        ## some optional side bar end ----------------------------

        content_frame.grid(row=1, column=0, padx=5, pady=5,)

        ## footer ---------------------------------------------

        footer_frame = ctk.CTkFrame(
            self.root.main_frame,
        )

        submit_button = ctk.CTkButton(
            footer_frame,
            text="Complete",
            width=150,
            command= self.set_student_as_completed,
            state="disabled" if self.alreadydid else "normal"
        )

        submit_button.grid(row=0, column=0, padx=0, pady=0)

        footer_frame.grid(row=2, column=0, padx=5, pady=5)

        ## footer end ------------------------------------------

    def set_student_as_completed(self):
        print("Adding Student Entry into database...")
        self.completion_database.addStudentEntry((self.student.username,))
        selection_screen(self.root, self.student)
