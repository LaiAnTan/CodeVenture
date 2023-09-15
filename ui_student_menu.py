import customtkinter as ctk

from App import App
from user.user_student import Student

class StudentMenuWindow():

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

        back_button = ctk.CTkButton(
            header_frame,
            text="Log Out",
            command=lambda : exit(),
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
