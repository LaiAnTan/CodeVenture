
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

    """
    Abstract base class for activity frames (module, quiz, challenge)
    """

    def __init__(self, activity: Activity, student: Student, editor_view=False):
        """
        Initializes the class.
        """

        super().__init__()
        self.ac = activity
        self.std = student
        self.editor_view = editor_view

        if student is None:
            self.editor_view = True

        self.completion_database = ActivityDictionary().getDatabase(self.ac.id)
        if not self.editor_view:
            self.done = self.completion_database.StudentEntryExist(self.std.getUsername())
        else:
            self.done = False

    def refresh_variables(self):
        """
        Resets variables to their default state.
        """

        if not self.editor_view:
            self.done = self.completion_database.StudentEntryExist(self.std.getUsername())

    def attach_elements(self) -> None:
        """
        Performs attachment of frame elements onto the main frame in root.

        @return None
        """
        self.SetFrames()

    def SetFrames(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.content_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.content_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.footer_frame = ctk.CTkFrame(self, fg_color='transparent')

        if self.editor_view == False:
            self.footer_frame.grid(row=2, column=0, padx=5, pady=5,
                                   sticky='nsew')

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

    def ImageHandler(self, content, max_img_height, max_img_width, attach_to,
                     source=None):
        """
        Function that handles displaying images.
        """
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
