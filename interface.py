import customtkinter as ctk

class UI:

    """
    user interface class that follows the singleton pattern
    """

    _instance = None

    main = ctk.CTk()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    frame = ctk.CTkFrame(main)
    main.title("CodeVenture - Development Build")

    main.minsize(900, 600)

    def	__new__(cls):
        """
        Initializer for class variables
        """
        if cls._instance:
            return cls._instance
        cls._instance = super(UI, cls).__new__(cls)
        return cls._instance
