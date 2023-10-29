import os
import customtkinter as ctk
from PIL import Image

from .ui_app import App
from .ui_app_frame import App_Frame
from ..backend.user.user_student import Student
from config import PFP_DIR, ASSET_DIR, LIGHTMODE_GRAY, DARKMODE_GRAY


def find_profile_pic(username: str) -> str:
    """
    Function that locates the profile picture of a student when given the
    username as input.
    """

    files = os.listdir(PFP_DIR)

    for file in files:
        if file.split(".")[0] == username:
            return f"{PFP_DIR}/{file}"

    return ""


class ProfileWindow(App_Frame):

    """
    Frame class for displaying the profile window.
    """

    header_height = 20
    full_width = 450
    half_width = full_width / 2
    full_content_height = 460 - header_height
    half_content_height = full_content_height / 2

    def __init__(self, student: Student) -> None:
        """
        Initializes the class.
        """
        super().__init__()
        self.student = student
        self.profile_pic_path = find_profile_pic(self.student.getUsername())
        self.cant_display_img_path = f"{ASSET_DIR}/cant_display_image.png"

        self.attach_elements()

    def refresh_variables(self):
        pass

    def attach_elements(self) -> None:
        """
        Performs attachment of frame elements onto the main frame in root.

        @return None
        """

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 2), weight=35)

        pad = ctk.CTkFrame(self, fg_color='transparent')
        pad.grid(row=0, column=0, rowspan=2, sticky='nsew')

        pad = ctk.CTkFrame(self, fg_color='transparent')
        pad.grid(row=0, column=2, rowspan=2, sticky='nsew')

        # header details -------------------------------------------

        header_frame = ctk.CTkFrame(
            self,
            width=self.full_width,
            height=self.header_height,
            fg_color="transparent"
        )

        header_frame.grid(
            row=0,
            column=1,
            sticky="swe",
            padx=5,
            pady=5
        )

        profile_title = ctk.CTkLabel(
            header_frame,
            text=f"Dashboard: {self.student.username}'s profile"
        )

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda: App().go_back_history(),
            width=20
        )

        profile_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5
        )

        back_button.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )

        # main content frame

        content_frame = ctk.CTkFrame(
            self,
            width=self.full_width,
            height=self.full_content_height,
            fg_color="transparent"
        )
        content_frame.columnconfigure((0, 1), weight=1)

        content_frame.grid(
            row=1,
            column=1,
            sticky='new'
        )

        # user details

        user_details_frame = ctk.CTkFrame(
            content_frame,
            width=self.half_width,
            height=self.half_content_height,
            fg_color=LIGHTMODE_GRAY if
            App().settings.getSettingValue("lightmode").lower() == "true" else
            DARKMODE_GRAY
        )

        user_details_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        try:
            img = Image.open(self.profile_pic_path)
        except Exception:
            img = Image.open(self.cant_display_img_path)

        user_profile_pic = ctk.CTkLabel(user_details_frame,
                                        text="",
                                        image=ctk.CTkImage(img,
                                                           size=(150, 150)))

        user_profile_pic.grid(row=0,
                              rowspan=2,
                              column=0,
                              padx=5,
                              pady=20)

        user_details_label = ctk.CTkLabel(
            user_details_frame,
            justify="left",
            wraplength=210,
            text=f"""Name: {self.student.getName()}
Date of birth: {self.student.getDateOfBirth()}
Email: {self.student.getEmail()}
Subscription: {self.student.getSubscriptionStatus()}
Subscription End Date: {self.student.getSubscriptionEndDate()}
""")

        user_details_label.grid(
            row=2,
            rowspan=2,
            column=0,
            padx=20,
            pady=5,
        )

        # completion frame

        completion_frame = ctk.CTkFrame(
            content_frame,
            width=self.half_width,
            height=self.half_content_height,
            fg_color="transparent"
        )
        completion_frame.columnconfigure(0, weight=1)
        completion_frame.rowconfigure(1, weight=1)
        completion_frame.grid(
            row=0,
            column=1,
            sticky='nsew'
        )

        # completion header

        completion_header_frame = ctk.CTkFrame(
            completion_frame,
            width=self.half_width,
            height=self.header_height,
            fg_color='transparent'
        )

        completion_header_frame.grid(
            row=0,
            column=0,
            sticky="nwe"
        )

        completion_title = ctk.CTkLabel(
            completion_header_frame,
            justify="left",
            text="Completed Activities",
            fg_color='transparent'
        )

        completion_title.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        completion_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5,
        )

        # completion content

        completion_content_frame = ctk.CTkScrollableFrame(
            completion_frame,
            # width=self.half_width,
            # height=self.half_content_height - self.header_height,
            fg_color="transparent"
        )

        completion_content_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )


if __name__ == "__main__":
    App().change_frame(ProfileWindow(Student('teststd')))
    App().mainloop()
