import customtkinter as ctk

from src.frontend.ui_app import App
from src.frontend.ui_std_window_gen import dispatcher
from src.backend.user.user_student import Student
from src.backend.database.database_activity import ActivityDB

from config import LIGHTMODE_GRAY, DARKMODE_GRAY


class ActivityTile(ctk.CTkFrame):

    """
    Class for activity tiles.

    Consists of a frame which displays summarized information of
    an activity.
    """

    font = ("Helvetica", 12)

    def __init__(self, id: str, width: int, height: int, student: Student,
                 master: ctk.CTkFrame, main_attach: App):
        super().__init__(master,
                         width=width,
                         height=height,
                         fg_color=LIGHTMODE_GRAY if
                         main_attach.settings.getSettingValue("lightmode")
                         .lower() == "true" else DARKMODE_GRAY
                         )
        self.root = main_attach
        self.master_frame = master  # master frame is not root.main_frame
        self.id = id
        self.student = student
        self.width = width
        self.height = height

        # fetch data
        adb = ActivityDB()

        self.name = adb.fetch_attr("title", self.id)
        self.type = adb.fetch_attr("type", self.id)
        self.difficulty = adb.fetch_attr("difficulty", self.id)
        self.tags = adb.fetch_attr("tags", self.id)

    def attach_elements(self):

        """
        Attaches the elements to the frame (self).
        """

        # master frame is self, because class inherits tkinter Frame

        name_label = ctk.CTkLabel(self,
                                  text=self.name,
                                  font=self.font,
                                  justify="center",
                                  width=self.width,
                                  wraplength=self.width
                                  )

        name_label.grid(row=0,
                        column=0,
                        padx=5,
                        pady=5,
                        )

        difficulty_label = ctk.CTkLabel(self,
                                        text=f"Difficulty: {self.difficulty}",
                                        font=self.font,
                                        justify="left",
                                        anchor="w",
                                        width=self.width,
                                        wraplength=self.width
                                        )

        difficulty_label.grid(row=1,
                              column=0,
                              padx=3,
                              )

        tags_label = ctk.CTkLabel(self,
                                  text=f"Tags: {self.tags}",
                                  font=self.font,
                                  justify="left",
                                  anchor="w",
                                  width=self.width,
                                  wraplength=self.width
                                  )

        tags_label.grid(row=2,
                        column=0,
                        padx=3,
                        )

        # quick access button

        def quickButtonEvent():
            dispatcher(self.id, self.type, self.root, self.student)

        quick_button = ctk.CTkButton(self,
                                     text="Go",
                                     font=self.font,
                                     width=int(self.width / 2),
                                     height=int(self.height / 10),
                                     command=lambda: quickButtonEvent())

        quick_button.grid(row=3,
                          column=0,
                          padx=5,
                          pady=5,
                          )
