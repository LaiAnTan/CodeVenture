import customtkinter as ctk

from .ui_app_frame import App_Frame
from .ui_app import App
from src.frontend.ui_std_window_gen import loginPage
from src.backend.user.user_student import Student
from src.backend.database.database_student import StudentDB


class SubscribeWindow(App_Frame):

    """
    Frame class for displaying the subscribe window.
    """

    full_width = 450
    half_width = full_width / 2

    def __init__(self, student: Student) -> None:
        """
        Initializes the class.
        """
        super().__init__()
        self.student = student

        self.attach_elements()

    def refresh_variables(self):
        pass

    def attach_elements(self) -> None:
        """
        Performs attachment of frame elements onto the main frame in root.

        @return None
        """

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 2), weight=1)
        # title frame

        title_frame = ctk.CTkFrame(
            self,
            width=self.full_width,
            height=40,
            fg_color="transparent"
        )

        title_frame.grid(
            row=0,
            column=0,
            sticky="sew"
        )

        title_frame.rowconfigure((0, 1), weight=1)
        title_frame.columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            title_frame,
            text="YOU HAVE NOT SUBSCRIBED",
            font=("Helvetica Bold", 30),
            anchor=ctk.CENTER,
        )

        title_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky=""
        )

        subtext_label = ctk.CTkLabel(
            title_frame,
            text="Please subscribe to gain access to CodeVenture.",
            font=("Helvetica", 18, "bold"),
            justify=ctk.CENTER,
        )

        subtext_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=20,
            sticky=""
        )

        # entry frame

        entry_frame = ctk.CTkFrame(
            self,
            width=self.full_width,
            height=100,
            fg_color="transparent"
        )

        entry_frame.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        entry_frame.rowconfigure((0, 1), weight=1)
        entry_frame.columnconfigure((0, 1), weight=1)

        sub_code = ctk.CTkEntry(
            entry_frame,
            width=int(self.full_width * 0.5),
            height=20,
            placeholder_text="Enter Activation Code",
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        sub_code.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky='e'
        )

        def validateSubButtonEvent() -> None:
            """
            Function that handles the event when the validate code button is
            pressed.
            """
            code = sub_code.get()
            if code == "99999":
                sdb = StudentDB()
                sdb.update_attr("subscription", self.student.getUsername(), 1)
                sdb.update_attr("subscription_end", self.student.getUsername(),
                                "hehe")
                loginPage()

        validate_sub_button = ctk.CTkButton(
            entry_frame,
            height=20,
            text="Validate Code",
            font=("Helvetica", 14),
            command=lambda: validateSubButtonEvent()
        )

        validate_sub_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky='w'
        )

        # buttons frame

        button_frame = ctk.CTkFrame(
            self,
            width=self.full_width,
            height=20,
            fg_color="transparent"
        )

        button_frame.grid(
            row=2,
            column=0,
            sticky="n"
        )

        button_frame.rowconfigure(0, weight=1)
        button_frame.columnconfigure((0, 1), weight=1)

        def subscribeButtonEvent():
            """
            Function that handles the event when the subscribe button is
            pressed.
            """
            print("This button relocates to the subscription service")
            return

        subscribe_button = ctk.CTkButton(
            button_frame,
            text="Subscribe",
            font=("Helvetica", 14),
            width=120, height=50,
            command=lambda: subscribeButtonEvent()
            )

        subscribe_button.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        def backToLoginButtonEvent():
            """
            Function that handles the event when the back to login button is
            pressed.
            """
            loginPage()

        back_to_login_button = ctk.CTkButton(
            button_frame,
            text="Back to Login",
            font=("Helvetica", 14),
            width=120,
            height=50,
            command=lambda: backToLoginButtonEvent()
            )

        back_to_login_button.grid(
            row=0,
            column=1,
            padx=20,
            pady=20
        )


if __name__ == "__main__":
    App().change_frame(SubscribeWindow(Student("test")))
    App().mainloop()
