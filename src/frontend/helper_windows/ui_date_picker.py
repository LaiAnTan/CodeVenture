
import customtkinter as ctk
from ..ui_app import App
from tkcalendar import Calendar


class DatePickerWindow(ctk.CTkToplevel):

    def __init__(self, a: App, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = 400
        self.height = 300
        self.geometry(f"{self.width}x{self.height}")

        self.date = None
        self.title("Date Picker")

    def getSelectedDate(self):
        return self.date

    def show_window(self):

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(
            self,
            width=self.width,
            height=self.height,
            fg_color="transparent"
        )

        main_frame.grid(
            row=0,
            column=0
        )

        title = ctk.CTkLabel(
            main_frame,
            text="Select Date",
            font=("Helvetica Bold", 30),
            anchor=ctk.CENTER
        )

        title.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        cal = Calendar(
            main_frame,
            selectmode='day'
        )

        cal.grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        def buttonEvent():
            dt = cal.selection_get()
            self.date = dt.strftime("%d/%m/%Y")
            self.destroy()

        button = ctk.CTkButton(
            main_frame,
            text="Done",
            font=("Helvetica", 14),
            width=80,
            height=30,
            command=lambda: buttonEvent()
        )

        button.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )
