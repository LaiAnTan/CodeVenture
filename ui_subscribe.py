from user.user_student import Student

from ui_window_gen import loginPage
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

        ## title frame

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

        entry_frame.rowconfigure((0, 1), weight=1)
        entry_frame.columnconfigure((0, 1), weight=1)

        sub_code = ctk.CTkEntry(
            entry_frame,
            width=int(full_width * 0.5),
            height=20,
            placeholder_text="Enter Activation Code", 
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        sub_code.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )
        
        def validateSubButtonEvent():
            pass

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
            pady=10
        )

        # buttons frame

        button_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=20,
            fg_color="transparent"
        )

        button_frame.grid(
            row=3,
            column=0,
            sticky="ew"
        )

        button_frame.rowconfigure(0, weight=1)
        button_frame.columnconfigure((0, 1), weight=1)

        def subscribeButtonEvent():
            print("This button relocates to the subscription service")
            pass

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
            loginPage(attach)

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
