
import customtkinter as ctk
from App import App
from tkcalendar import Calendar

class DatePickerWindow(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

