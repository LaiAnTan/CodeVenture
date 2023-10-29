import customtkinter as ctk

from .ui_app_frame import App_Frame
from ..backend.user.user_student import Student
from .helper_windows.ui_activity_tile import ActivityTile
from .helper_windows.ui_more_info_tile import MoreInfoTile
from .ui_std_window_gen import loginPage, profilePage, settingsPage
from .helper_windows.ui_recommended_ac_tile import RecommendedAcFrame


class StudentMenuWindow(App_Frame):

    """
    Frame class for displaying the student menu.
    """

    # constants
    header_height = 35
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
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure(0, weight=1)

        # header frame

        header_frame = ctk.CTkFrame(
            self,
            width=self.full_width,
            height=self.header_height,
            fg_color="transparent"
        )
        header_frame.pack_propagate(False)

        profile_title = ctk.CTkLabel(
            header_frame,
            text=f"Logged in as: {self.student.username}"
        )

        profile_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5,
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
            sticky="s",
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
            sticky="n"
        )

        content_frame.rowconfigure((0, 1), weight=1)
        content_frame.columnconfigure(0, weight=1)

        # recommended

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

        # recommend frame

        ac_tile_width = 120
        ac_tile_height = 220

        recommended_frame = RecommendedAcFrame(
            content_frame,
            width=self.full_width,
            height=ac_tile_width + 35,
            orientation='horizontal'
        )

        recommended_frame.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        ac_id = ["MD0000", "QZ0000", "CH0000"]

        for index, id in enumerate(ac_id):
            recommended = ActivityTile(
                id,
                ac_tile_width,
                ac_tile_height,
                self.student,
                recommended_frame,
            )
            recommended.attach_elements()
            recommended.grid(
                row=0,
                column=index,
                padx=10,
                pady=10
            )

        recommend_fake_dots = MoreInfoTile(
            30,
            ac_tile_height,
            recommended_frame
        )
        recommend_fake_dots.attach_elements()
        recommend_fake_dots.grid(row=0,
                                 column=len(ac_id),
                                 padx=10,
                                 pady=10,
                                 sticky='ns')

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
