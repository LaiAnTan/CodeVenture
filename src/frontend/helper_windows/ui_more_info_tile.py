import customtkinter as ctk

from ..ui_app import App
from ...backend.user.user_student import Student

from config import LIGHTMODE_GRAY, DARKMODE_GRAY


class MoreInfoTile(ctk.CTkFrame):

    """
    Class for activity tiles.

    Consists of a frame which displays summarized information of
    an activity.
    """

    font = ("Helvetica", 12)

    def __init__(self, width: int, height: int, master: ctk.CTkFrame):
        super().__init__(master,
                         width=width,
                         height=height,
                         fg_color=LIGHTMODE_GRAY if
                         App().settings.getSettingValue("lightmode")
                         .lower() == "true" else DARKMODE_GRAY
                         )
        self.master_frame = master  # master frame is not root.main_frame
        self.width = width
        self.height = height

    def attach_elements(self):

        """
        Attaches the elements to the frame (self).
        """
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # master frame is self, because class inherits tkinter Frame

        name_label = ctk.CTkLabel(self,
                                  text="...",
                                  font=self.font,
                                  justify="center",
                                  width=self.width,
                                  wraplength=self.width
                                  )

        name_label.grid(row=0, column=0, padx=5, pady=5)