
import customtkinter as ctk
from abc import abstractmethod, ABC

from ..ui_app import App
from ..ui_app_frame import App_Frame
from ...backend.activity.ac_classes.ac_activity import Activity
from ...backend.user.user_student import Student
from ...backend.activity.ac_database.db_ac_completed import ActivityDictionary

from .helper_class.code_runner import CodeRunner
from .helper_class.imagelabel import ImageLabel

class ActivityWindow(App_Frame, ABC):

    def __init__(self, activity: Activity, student: Student):
        super().__init__()
        self.ac = activity
        self.std = student
        self.completion_database = ActivityDictionary().getDatabase(self.ac.id)
        
        self.done = self.completion_database.StudentEntryExist(self.std.getUsername())

    def refresh_variables(self):
        self.done = self.completion_database.StudentEntryExist(self.std.getUsername())

    def attach_elements(self):
        self.SetFrames()

    def SetFrames(self):
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=5, pady=5)

        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid(row=2, column=0, padx=5, pady=5)

        self.SetHeader()
        self.SetContent()
        self.SetFooter()

    def SetHeader(self):
        name = ctk.CTkLabel(
            self.header_frame,
            text=f"{self.ac.id} {self.ac.title}"
        )
        name.pack(side=ctk.LEFT, padx=5, pady=5)

        back_button = ctk.CTkButton(
            self.header_frame,
            text="Back",
            command=lambda: App().go_back_history(),
            width=20
        )
        back_button.pack(side=ctk.RIGHT, padx=5, pady=5)

    @abstractmethod
    def SetContent(self):
        pass

    @abstractmethod
    def SetFooter(self):
        pass

    # HELPER FUNCTIONS

    def ImageHandler(self, content, max_img_height, max_img_width, attach_to, source=None):
        if source is None:
            source = self.ac
        
        if source.img.get(content):
            ret_widget = ImageLabel(
                attach_to,
                f"{source.ModulePath}/{source.img[content]}",
                max_img_height - 50,
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

    def CodeHandler(self, content, max_img_width, attach_to, source=None):
        if source is None:
            source = self.ac

        if source.code.get(content):
            ret_widget = CodeRunner(
                attach_to,
                max_img_width - 30,
                source.code[content],
                source.ModulePath
            )
        else:
            ret_widget = ctk.CTkLabel(
                attach_to,
                text=f"Error displaying code {content}",
                width=max_img_width,
                wraplength=max_img_width - 10,
            )
        return ret_widget