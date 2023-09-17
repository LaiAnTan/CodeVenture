import customtkinter as ctk

from ui_window_gen import loginPage, profilePage, settingsPage, loadingPage
from App import App
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
            height=header_height
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
            loadingPage(attach, Student(None), "loginPage", ["Logging out...", "Clearing session coookies..", "Nuking search history and bookmarks!"])

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
            loadingPage(attach, self.student, "settingsPage", ["Loading settings page...", "Loading settings page..", "Loading settings page."])

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
            loadingPage(attach, self.student, "profilePage", ["Fetching profile details...", "Fetching profile details..", "Fetching profile details."])

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
            height=full_content_height
        )

        content_frame.grid(
            row=1,
            column=0
        )

        ## search bar

        ## recommended

        ## buttons
