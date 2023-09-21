import customtkinter as ctk
from ui_std_window_gen import loginPage, profilePage, settingsPage
from ui_app import App
from user.user_student import Student

class StudentMenuWindow:

    def __init__(self, student: Student):
            self.student = student

    def FillFrames(self, attach: App):

        attach.main_frame.grid(
            row=0,
            column=0
        )

        header_height = 20
        full_width = 450
        half_width = full_width / 2
        full_content_height = 460 - header_height
        half_content_height = full_content_height / 2


        ## header details -------------------------------------------

        header_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=header_height,
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
            loginPage(attach)

        logout_button = ctk.CTkButton(
            header_frame,
            text="Log Out",
            command=lambda : logoutButtonEvent(),
            width=20
        )

        logout_button.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )

        def settingsButtonEvent():
            settingsPage(attach, self.student)

        settings_button = ctk.CTkButton(
            header_frame,
            text="Settings",
            command=lambda : settingsButtonEvent(),
            width=20
        )

        settings_button.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )

        def profileButtonEvent():
            profilePage(attach, self.student)

        profile_button = ctk.CTkButton(
            header_frame,
            text="Profile",
            command=lambda : profileButtonEvent(),
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

        ## header details end --------------------------------------------

        ## main content frame

        content_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=full_content_height,
            fg_color="transparent"
        )

        content_frame.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        ## search bar

        search_bar_frame = ctk.CTkFrame(
            content_frame,
            width=full_width,
            fg_color="transparent",
            height=30
        )

        search_bar_frame.grid(
            row=0,
            column=0,
            sticky="ew"
        )


        search_bar = ctk.CTkEntry(
            search_bar_frame,
            width= int(full_width * 0.75),
            placeholder_text="Looking for something?",
            font=("Helvetica", 14),
            justify=ctk.LEFT
        )

        search_bar.pack(
            side=ctk.LEFT,
            padx=5,
        )

        def searchButtonEvent():
            pass

        search_button = ctk.CTkButton(
            search_bar_frame,
            text="Search",
            command=lambda : searchButtonEvent(),
            width=20
        )

        search_button.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5,
        )

        ## recommended

        recommended_frame = ctk.CTkFrame(
            content_frame,
            width=full_width,
        )

        recommended_title = ctk.CTkLabel(
            recommended_frame,
            text="Recommended modules:",
            font=("Helvetica", 14),
        )

        recommended_title.grid(
            row=0,
            column=0,
            sticky="e",
            padx=10,
            pady=10,
        )

        recommended_frame.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        ## buttons

        buttons_frame = ctk.CTkFrame(
            content_frame,
            width=full_width
        )

        buttons_frame.grid(
            row=3,
            column=0,
            sticky="ew"
        )

        from ui_std_window_gen import displayActivitySelections

        all_activities = ctk.CTkButton(
            buttons_frame,
            width=40,
            text="All Activities",
            command=lambda : displayActivitySelections(attach, self.student)
        )

        all_activities.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        buttons_frame.columnconfigure(0, weight=1)


