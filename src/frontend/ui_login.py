import customtkinter as ctk

from .ui_app_frame import App_Frame
from .ui_std_window_gen import registerPage, studentMenuPage, subscribePage, \
    studentProfileSetupPage
from .ui_edu_window_gen import editor_prompt
from ..backend.user.user_base import User
from ..backend.user.user_student import Student


class LoginWindow(App_Frame):

    """
    Frame class for displaying the login window.
    """

    def __init__(self) -> None:
        """
        Initializes the class.
        """

        super().__init__()
        self.username = None
        self.password = None
        self.user = User(None)

        self.attach_elements()

    def getUsername(self):
        """
        Getter for username.
        """
        return self.username

    def getPassword(self):
        """
        Getter for password.
        """
        return self.password

    def refresh_variables(self):
        pass

    def attach_elements(self):
        """
        Performs attachment of frame elements onto the main frame in root.

        @return None
        """

        self.rowconfigure((0, 2), weight=1)
        self.columnconfigure(0, weight=1)

        # title frame

        title_frame = ctk.CTkFrame(
            self,
            # width=full_width,
            # height=40,
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
            text="CodeVenture",
            font=("Helvetica Bold", 30),
            anchor=ctk.CENTER,
        )

        title_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
        )

        login_label = ctk.CTkLabel(
            title_frame,
            text="LOGIN",
            font=("Helvetica", 18, "bold"),
            justify=ctk.CENTER,
        )

        login_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=20,
        )

        # entry frame

        entry_frame = ctk.CTkFrame(
            self,
            # width=full_width,
            # height=100,
            fg_color="transparent",
        )

        entry_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        entry_frame.columnconfigure(0, weight=1)

        username1 = ctk.CTkEntry(
            entry_frame,
            height=20,
            placeholder_text="Username",
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        username1.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky='n'
        )

        password1 = ctk.CTkEntry(
            entry_frame,
            height=20,
            placeholder_text="Password",
            show="•",
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        password1.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky='n'
        )

        # show password checkbox

        checkbox1_status = ctk.IntVar(value=0)

        def eventShowPassword():
            """
            Handles event when show password checkbox is ticked / unticked.
            """
            if checkbox1_status.get() == 1:
                password1.configure(show="")
            else:
                password1.configure(show="•")
            password1.update()

        checkbox1 = ctk.CTkCheckBox(
            entry_frame,
            text="Show password",
            font=("Helvetica", 14),
            variable=checkbox1_status,
            onvalue=1,
            offvalue=0,
            command=lambda: eventShowPassword(),
        )

        checkbox1.grid(
            row=2,
            column=0,
            padx=10,
            pady=(10, 20),
            sticky='n'
        )

        wrong_password_label = ctk.CTkLabel(
            entry_frame,
            text="Invalid username or password, Try again.",
            font=("Helvetica", 14),
            text_color="#FF0000",
            anchor=ctk.CENTER
        )

        # buttons frame

        button_frame = ctk.CTkFrame(
            self,
            # width=full_width,
            # height=20,
            fg_color="transparent"
        )

        button_frame.rowconfigure(0, weight=1)
        button_frame.columnconfigure((0, 1), weight=1)

        button_frame.grid(
            row=2,
            column=0,
            sticky="new"
        )

        def loginButtonEvent():
            """
            Handles login event when button is pressed
            """
            self.username = username1.get()
            self.user.setUsername(self.username)
            if self.user.login(password1.get()) is True:
                print(f"Logged in {self.username}")
                print(f"Type: {self.user.getUserType()}")

                match self.user.getUserType():

                    case "student":

                        s = Student(self.user.getUsername())

                        if s.getProfileSetupStatus() is True:
                            print("hehe")
                            studentProfileSetupPage(s)
                        elif s.isSubscribed() is False:
                            subscribePage(s)
                        else:
                            studentMenuPage(s)

                    case "educator":
                        editor_prompt()

                    case "admin":
                        return

                    case _:
                        raise AssertionError("Unknown user type")

            else:
                print("Login failed, Incorrect username or password")
                wrong_password_label.grid(
                    row=3,
                    column=0,
                    padx=5,
                    pady=5
                )

        login_button = ctk.CTkButton(
            button_frame,
            text="Login",
            font=("Helvetica", 14),
            width=120,
            height=50,
            command=lambda: loginButtonEvent()
            )

        login_button.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky='e'
        )

        def registerButtonEvent():
            """
            Function that handles the event when the register button is
            pressed.
            """
            registerPage()

        register_button = ctk.CTkButton(
            button_frame,
            text="Register",
            font=("Helvetica", 14),
            width=120, height=50,
            command=lambda: registerButtonEvent()
            )

        register_button.grid(
            row=0,
            column=1,
            padx=20,
            pady=20,
            sticky='w'
        )
