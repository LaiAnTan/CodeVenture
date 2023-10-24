import customtkinter as ctk
from argon2 import PasswordHasher, exceptions

from .ui_std_window_gen import studentMenuPage
from .ui_app import App
from .ui_app_frame import App_Frame
from ..backend.user.user_student import Student
from ..backend.database.database_user import UserDB


def changePasswordHandler(student: Student, old_password: str,
                          new_password: str, confirm_password: str):
    """
    Handles password change of a user.

    returns a 2-tuple with the first value being a boolean and the second value
    being the message to display.
    """
    db = UserDB()

    current_pw_hash = db.fetch_attr("password", student.getUsername())

    if old_password == "" or new_password == "" or confirm_password == "":
        return (False, "One or more fields empty")

    if old_password == new_password:
        return (False, "Old password same as new password")

    if new_password != confirm_password:
        return (False, "Passwords do not match")

    ph = PasswordHasher()

    try:
        ph.verify(current_pw_hash, old_password)
    except exceptions.VerifyMismatchError:
        return (False, "Wrong password")

    db.update_attr("password", student.getUsername(), ph.hash(new_password))

    return (True, "Password Change Successful")


class SettingsWindow(App_Frame):

    header_height = 20
    full_width = 600
    half_width = full_width / 2
    full_content_height = 460 - header_height
    half_content_height = full_content_height / 2

    def __init__(self, student: Student):
        super().__init__()

        self.student = student
        self.attach_elements()

    def refresh_variables(self):
        pass

    def attach_elements(self):

        # header details -------------------------------------------

        header_frame = ctk.CTkFrame(
            self,
            width=self.full_width,
            height=self.header_height
        )

        header_frame.grid(
            row=0,
            column=0,
            sticky="we",
            padx=5,
            pady=5
        )

        settings_title = ctk.CTkLabel(
            header_frame,
            text="Settings"
        )

        settings_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5
        )

        def backButtonEvent():
            studentMenuPage(self.student)

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda: App().go_back_history(),
            width=20
        )

        back_button.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )

        # header details end --------------------------------------------

        # main content frame

        content_frame = ctk.CTkFrame(
            self,
            width=self.full_width,
            height=self.full_content_height,
            fg_color="transparent"
        )

        content_frame.grid(
            row=1,
            column=0
        )

        # change appearance mode

        toggle_appearance_mode_frame = ctk.CTkFrame(
            content_frame,
            width=self.full_width,
            height=self.header_height
        )

        toggle_appearance_mode_frame.grid(
            row=0,
            column=0,
            sticky="we",
            padx=5,
            pady=5
        )

        toggle_appearance_mode_frame.rowconfigure((0), weight=1)
        toggle_appearance_mode_frame.columnconfigure((0, 1), weight=1)

        toggle_appearance_mode_title = ctk.CTkLabel(
            toggle_appearance_mode_frame,
            text="Toggle light mode"
        )

        toggle_appearance_mode_title.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="e"
        )

        appearance_toggler_status = ctk.IntVar(value=0)

        def appearanceTogglerEvent():
            if appearance_toggler_status.get() == 1:
                ctk.set_appearance_mode("light")
                ctk.set_default_color_theme("blue")
                App().settings.updateSetting("lightmode", "true")

            else:
                ctk.set_appearance_mode("dark")
                ctk.set_default_color_theme("dark-blue")
                App().settings.updateSetting("lightmode", "false")

            App().main.update_idletasks()

        appearance_toggler = ctk.CTkSwitch(
            toggle_appearance_mode_frame,
            onvalue=1,
            offvalue=0,
            text="Light mode on",
            variable=appearance_toggler_status,
            command=lambda: appearanceTogglerEvent(),
        )

        if App().settings.getSettingValue("lightmode").lower() == "true":
            print("lightmode enabled")
            appearance_toggler.select()

        appearance_toggler.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # change password

        change_password_frame = ctk.CTkFrame(
            content_frame,
            width=self.full_width,
        )

        change_password_frame.grid(
            row=1,
            column=0,
            sticky="we",
            padx=5,
            pady=5,
        )

        change_password_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        change_password_frame.columnconfigure((0), weight=1)

        change_password_label = ctk.CTkLabel(
            change_password_frame,
            text="Change Password",
            font=("Helvetica", 14),
        )

        change_password_label.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        old_password = ctk.CTkEntry(
            change_password_frame,
            height=20,
            placeholder_text="Old password",
            font=("Helvetica", 14),
            justify=ctk.CENTER,
            show="•",
        )

        old_password.grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        new_password = ctk.CTkEntry(
            change_password_frame,
            height=20,
            placeholder_text="New password",
            font=("Helvetica", 14),
            justify=ctk.CENTER,
            show="•",
        )

        new_password.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )

        confirm_password = ctk.CTkEntry(
            change_password_frame,
            height=20,
            placeholder_text="Confirm password",
            font=("Helvetica", 14),
            justify=ctk.CENTER,
            show="•",
        )

        confirm_password.grid(
            row=3,
            column=0,
            padx=10,
            pady=10
        )

        password_msg_label = ctk.CTkLabel(
            change_password_frame,
            text="",
            font=("Helvetica", 14),
            text_color="#FF0000",
            anchor=ctk.CENTER
        )

        def changePasswordButtonEvent():
            ret = changePasswordHandler(self.student, old_password.get(),
                                        new_password.get(),
                                        confirm_password.get())
            if ret[0] is True:
                password_msg_label.configure(text=ret[1], text_color="#00FF00")

            elif ret[0] is False:
                password_msg_label.configure(text=ret[1], text_color="#FF0000")

            password_msg_label.grid(
                row=4,
                column=0,
                padx=5,
                pady=5
            )

        update_password_button = ctk.CTkButton(
            change_password_frame,
            text="Update Password",
            font=("Helvetica", 14),
            width=100,
            height=40,
            command=lambda: changePasswordButtonEvent()
        )

        update_password_button.grid(
            row=5,
            column=0,
            padx=5,
            pady=5
        )
