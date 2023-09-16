import customtkinter as ctk

from ui_window_gen import studentMenuPage
from App import App
from user.user_student import Student

class SettingsWindow:

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

        header_frame.grid(
            row=0,
            column=0,
            sticky="we",
            padx=5,
            pady=5
        )

        settings_title = ctk.CTkLabel(
            header_frame,
            text=f"Settings"
        )

        settings_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5
        )

        def backButtonEvent():
            studentMenuPage(attach, self.student)

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda : backButtonEvent(),
            width=20
        )

        back_button.pack(
            side=ctk.RIGHT,
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

        ## change mode

        toggle_appearance_mode_frame = ctk.CTkFrame(
            content_frame,
            width=full_width,
            height=header_height
        )

        toggle_appearance_mode_frame.grid(
            row=0,
            column=0,
            sticky="we",
            padx=5,
            pady=5
        )

        toggle_appearance_mode_title = ctk.CTkLabel(
            toggle_appearance_mode_frame,
            text=f"Toggle light mode"
        )

        toggle_appearance_mode_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5
        )

        appearance_toggler_status = ctk.IntVar(value=0)

        def appearanceTogglerEvent():
            if appearance_toggler_status.get() == 1:
                ctk.set_appearance_mode("light")
                ctk.set_default_color_theme("blue")
                attach.settings.updateSetting("lightmode", "true")

            else:
                ctk.set_appearance_mode("dark")
                ctk.set_default_color_theme("dark-blue")
                attach.settings.updateSetting("lightmode", "false")

            attach.main.update_idletasks()

        appearance_toggler = ctk.CTkSwitch(
            toggle_appearance_mode_frame,
            onvalue=1,
            offvalue=0,
            text="Light",
            variable=appearance_toggler_status,
            command=lambda : appearanceTogglerEvent(),
        )

        if attach.settings.getSettingValue("lightmode").lower() == "true":
            print("lightmode enabled")
            appearance_toggler.select()

        appearance_toggler.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )
        toggle_appearance_mode_left_text = ctk.CTkLabel(
            toggle_appearance_mode_frame,
            text="Dark"
        )

        toggle_appearance_mode_left_text.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )

