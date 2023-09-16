from user.user_student import Student

from App import App
import customtkinter as ctk

class SubscribeWindow:

    def __init__(self, student: Student):
        self.student = student

    def FillFrames(self, attach: App):

        attach.main_frame.grid(
            row=0,
            column=0
        )

        full_width = 450
        half_width = full_width / 2

        title_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=40,
            fg_color="transparent"
        )

        title_frame.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        title_frame.rowconfigure((0,1), weight=1)
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
            attach.main_frame,
            width=full_width,
            height=100,
            fg_color="transparent"
        )

        entry_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        entry_frame.rowconfigure((0, 1, 2), weight=1)
        entry_frame.columnconfigure(0, weight=1)

        sub_code = ctk.CTkEntry(
            entry_frame,
            height=20,
            placeholder_text="Enter Subscription Code", 
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        sub_code.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )
