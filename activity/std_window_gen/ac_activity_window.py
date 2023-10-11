import customtkinter as ctk

from abc import abstractmethod

from ..ac_classes.ac_activity import Activity
from user.user_student import Student
from ui.ui_app import App
from ..ac_database.db_ac_completed import ActivityDictionary


class ActivityWindow(ctk.CTkFrame):

    def __init__(self, activity: Activity, student: Student, main_attach: App):
        super().__init__(main_attach.main_frame)
        self.root = main_attach

        self.ac = activity
        self.std = student
        self.completion_database = ActivityDictionary.getDatabase(self.ac.id)
        self.done = self.completion_database.StudentEntryExist(self.std.username)

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=5, pady=5)

        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid(row=2, column=0, padx=5, pady=5)

    def Attach(self):
        self.grid(row=0, column=0)

    def SetFrames(self):
        self.SetHeader()
        self.SetContent()
        self.SetFooter()

    def SetHeader(self):
        from ui.ui_std_window_gen import displayActivitySelections

        name = ctk.CTkLabel(
            self.header_frame,
            text=f"{self.ac.id} {self.ac.title}"
        )
        name.pack(side=ctk.LEFT, padx=5, pady=5)

        back_button = ctk.CTkButton(
            self.header_frame,
            text="Back",
            command=lambda: displayActivitySelections(self.root, self.std),
            width=20
        )
        back_button.pack(side=ctk.RIGHT, padx=5, pady=5)

    @abstractmethod
    def SetContent(self):
        pass

    @abstractmethod
    def SetFooter(self):
        pass
