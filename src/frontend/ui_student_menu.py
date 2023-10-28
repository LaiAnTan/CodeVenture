import customtkinter as ctk

from .ui_std_window_gen import loginPage, profilePage, settingsPage
from src.frontend.ui_activity_tile import ActivityTile
from .ui_app_frame import App_Frame
from ..backend.user.user_student import Student


class StudentMenuWindow(App_Frame):

    """
    Frame class for displaying the student menu.
    """

    # constants
    header_height = 20
    full_width = 450
    half_width = full_width / 2
    full_content_height = 460 - header_height
    half_content_height = full_content_height / 2

    def __init__(self, student: Student) -> None:
        """
        Initializes the class.

        @param student: student object coresponding to current user.
        @return None
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
        # header frame

        header_frame = ctk.CTkFrame(
            self,
            width=self.full_width,
            height=self.header_height,
            fg_color="transparent"
        )

        profile_title = ctk.CTkLabel(
            header_frame,
            text=f"Logged in as: {self.student.username}"
        )

        profile_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5
        )

        def logoutButtonEvent():
            """
            Function that handles the event when the logout button is
            pressed.
            """
            loginPage()

        logout_button = ctk.CTkButton(
            header_frame,
            text="Log Out",
            command=lambda: logoutButtonEvent(),
            width=20
        )

        logout_button.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )

        def settingsButtonEvent():
            """
            Function that handles the event when the settings button is
            pressed.
            """
            settingsPage(self.student)

        settings_button = ctk.CTkButton(
            header_frame,
            text="Settings",
            command=lambda: settingsButtonEvent(),
            width=20
        )

        settings_button.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )

        def profileButtonEvent():
            """
            Function that handles the event when the profile button is
            pressed.
            """
            profilePage(self.student)

        profile_button = ctk.CTkButton(
            header_frame,
            text="Profile",
            command=lambda: profileButtonEvent(),
            width=20
        )

        profile_button.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )

        header_frame.grid(
            row=0,
            column=0,
            sticky="we",
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

        content_frame.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        # recommended

        recommended_frame = ctk.CTkFrame(
            content_frame,
            width=self.full_width,
            fg_color="transparent"
        )

        recommended_title = ctk.CTkLabel(
            content_frame,
            text="Recommended modules:",
            font=("Helvetica", 14),
        )

        recommended_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=10,
        )

        recommended_frame.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        # recommended frame

        ac_tile_width = 120
        ac_tile_height = 220

        recommended_1 = ActivityTile("MD0000",
                                     ac_tile_width,
                                     ac_tile_height,
                                     self.student,
                                     recommended_frame,
                                     )

        recommended_1.attach_elements()

        recommended_1.grid(row=1,
                           column=0,
                           padx=10,
                           pady=10)

        recommended_2 = ActivityTile("QZ0000",
                                     ac_tile_width,
                                     ac_tile_height,
                                     self.student,
                                     recommended_frame,
                                     )

        recommended_2.attach_elements()

        recommended_2.grid(row=1,
                           column=1,
                           padx=10,
                           pady=10)

        recommended_3 = ActivityTile("CH0000",
                                     ac_tile_width,
                                     ac_tile_height,
                                     self.student,
                                     recommended_frame,
                                     )

        recommended_3.attach_elements()

        recommended_3.grid(row=1,
                           column=2,
                           padx=10,
                           pady=10)

        recommended_frame.rowconfigure((0, 1), weight=1)
        recommended_frame.columnconfigure((0, 1, 2), weight=1)

        # button frame

        buttons_frame = ctk.CTkFrame(
            content_frame,
            width=self.full_width,
            fg_color="transparent"
        )

        buttons_frame.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        from .ui_std_window_gen import displayActivitySelections

        all_activities = ctk.CTkButton(
            buttons_frame,
            width=40,
            text="All Activities",
            command=lambda: displayActivitySelections(self.student)
        )

        all_activities.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        buttons_frame.columnconfigure(0, weight=1)
