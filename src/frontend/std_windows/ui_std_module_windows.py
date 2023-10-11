
import customtkinter as ctk

from ..ui_app import App
from ..ui_std_window_gen import displayActivitySelections
from ..helper_windows.code_runner import CodeRunner
from ..helper_windows.imagelabel import ImageLabel
from ..std_windows.ui_std_activity_window import ActivityWindow
from ...backend.user.user_student import Student
from ...backend.activity.ac_classes.ac_module import Module
from ...backend.activity.ac_database.db_ac_completed import ActivityDictionary


class ModuleWindow(ActivityWindow):

    def __init__(self, module: Module, student: Student, main_attach: App):
        super().__init__(module, student, main_attach)

        self.SetFrames()

    def SetContent(self):
        main_content_frame_width = 550
        main_content_frame_height = 420

        self.contents = ctk.CTkScrollableFrame(
            self.content_frame, 
            width=main_content_frame_width,
            height=main_content_frame_height
        )
        self.contents.grid(row=0, column=0, padx=5, pady=5)

        paragraph_frame_width = main_content_frame_width - 20

        for index, content in enumerate(self.ac.content):
            paragraph_frame = ctk.CTkFrame(self.contents)
            paragraph_frame.grid(row=index, column=0, padx=5, pady=10)

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

    def SetFooter(self):
        submit_button = ctk.CTkButton(
            self.footer_frame,
            text="Complete",
            width=150,
            command= self.StudentCompletion,
            state="disabled" if self.done else "normal"
        )
        submit_button.grid(row=0, column=0, padx=0, pady=0)

    # helper functions

    def ImageHandler(self, content, max_img_width, attach_to):
        if self.ac.img.get(content):
            ret_widget = ImageLabel(
                attach_to,
                f"{self.ac.ModulePath}/{self.ac.img[content]}",
                max_img_width - 50,
            )
        else:
            ret_widget = ctk.CTkLabel(
                attach_to,
                text=f"Error displaying image {content}",
                width=max_img_width,
                wraplength=max_img_width - 10,
            )
        return ret_widget
    
    def CodeHandler(self, content, max_img_width, attach_to):
        if self.ac.code.get(content):
            ret_widget = CodeRunner(
                            attach_to,
                            max_img_width - 30,
                            self.ac.code[content],
                            self.ac.ModulePath
                            )
        else:
            ret_widget = ctk.CTkLabel(
                attach_to,
                text=f"Error displaying code {content}",
                width=max_img_width,
                wraplength=max_img_width - 10,
            )
        return ret_widget

    def StudentCompletion(self):
        print("Adding Student Entry into backend.database...")
        self.completion_backend.database.addStudentEntry((self.std.username,))
        displayActivitySelections(self.root, self.std)

if __name__ == "__main__":
    from ..ui_app import App

    ActivityDictionary()
    main = App()
    frame = ModuleWindow(Module("MD0000"), Student("test_student"), main)
    frame.Attach()
    main.main_frame.grid(row=0, column=0)
    main.mainloop()
