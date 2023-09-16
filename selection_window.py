import customtkinter as ctk

from app import App

from module import Module
from quiz import Quiz
from challenge import Challange

# u gotta be kidding me
# https://stackoverflow.com/questions/66662493/how-to-progress-to-next-window-in-tkinter

class SelectionScreen():
    @classmethod
    def attach_elements(cls, attach: App):
        cool_text = ctk.CTkLabel(
            attach.main_frame,
            text="Wow, Cool and Quirky Selection Window!!!",
            text_color="black",
            fg_color="#FFC0CB"
        )

        cool_text.grid(
            row=0,
            column=0,
            columnspan=3,
            padx=20,
            pady=20,
            sticky="ew"
        )

        from window_gen import module_screen

        module_button = ctk.CTkButton(
            attach.main_frame,
            text="Module Example",
            command=lambda : module_screen(Module("MD0000"), attach)
        )

        module_button.grid(
            row=1,
            column=0,
            padx=20,
            pady=20,
        )

        from window_gen import quiz_screen

        quiz_button = ctk.CTkButton(
            attach.main_frame,
            text="Quiz Example",
            command=lambda : quiz_screen(Quiz("QZ0000"), attach)
        )

        quiz_button.grid(
            row=1,
            column=1,
            padx=20,
            pady=20
        )

        from window_gen import challange_screen

        challange_button = ctk.CTkButton(
            attach.main_frame,
            text="Challange Example",
            command=lambda : challange_screen(Challange("CH0001"), attach)
        )

        challange_button.grid(
            row=1,
            column=2,
            padx=20,
            pady=20
        )

    @classmethod
    def __beep_boop(self) -> None:
        print("Button Pressed!")