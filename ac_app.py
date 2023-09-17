import customtkinter as ctk

class App():
    _instance = None

    width = 900
    height = 600

    main = ctk.CTk()

    main_frame = ctk.CTkFrame(
        main,
        width=width,
        height=height,
    )

    main.rowconfigure(0, weight=1)
    main.columnconfigure(0, weight=1)

    main.geometry(f"{width}x{height}")
    main.title("Fuck You")

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    main.minsize(width, height)
    main.maxsize(width, height)

    @classmethod
    def clean_frame(cls):
        print("Cleaning main_frame to render next frame")
        # cls.main_frame.place_forget()
        for widgets in cls.main_frame.winfo_children():
            widgets.destroy()

    @classmethod
    def __new__(cls, placeholder=None):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def mainloop(cls):
        cls.main.mainloop()

if __name__ == "__main__":
    test = App()
    test.mainloop()