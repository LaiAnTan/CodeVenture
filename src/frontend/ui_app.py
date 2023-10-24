import customtkinter as ctk

from ..backend.settings.settings import Settings
from config import ROOT_DIR


class App():
    _instance = None

    width = 900
    height = 600

    main = ctk.CTk()
    main.rowconfigure(0, weight=1)
    main.columnconfigure(0, weight=1)

    history = []

    main_frame = ctk.CTkFrame(
            main,
            width=width,
            height=height,
            fg_color="transparent"
        )
    main_frame.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)

    main.geometry(f"{width}x{height}")
    main.title("CodeVenture")

    main.minsize(width, height)
    main.maxsize(width, height)

    settings = Settings(f"{ROOT_DIR}/settings.conf")

    if settings.getSettingValue("lightmode").lower() == "false":
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
    elif settings.getSettingValue("lightmode").lower() == "true":
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    @classmethod
    def clean_frame(cls):
        """Call this before adding new frames
        
        remove all frames from the App's main frame
        
        DO NOT call this after adding your new frame"""
        # cls.main_frame.place_forget() # i dont think this is doing anything?
        cls.main_frame.grid_forget() # THIS is the one that is doing something
        # but that breaks so :P
        for widgets in cls.main_frame.winfo_children():
            widgets.grid_forget()

    @classmethod
    def go_back_history(cls):
        # remove current frame from history (removed forever)
        cls.history.pop()
        previous = cls.history[-1]

        cls.clean_frame()
        previous.refresh()
        cls.change_frame(previous)

    @classmethod
    def add_to_history(cls, frame):
        cls.history.append(frame)

    @classmethod
    def change_frame(cls, new_frame):
        """Changes frame of App
        Call App().clean_frame beforehand to remove existing 
        windows

        make sure new_frame's master is App or App.main_frame

        
        Please call this if you want to change the frame of the App, do
        not attempt to grid it by yourself, the back buttons depend on this"""
        cls.add_to_history(new_frame)
        new_frame.grid(row=0, column=0)
        cls.main_frame.grid(row=0, column=0)

    @classmethod
    def __new__(cls, placeholder=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def mainloop(cls):
        cls.main.mainloop()


if __name__ == "__main__":
    test = App()
    test2 = App()
    print(test2 is test)

    test.mainloop()
