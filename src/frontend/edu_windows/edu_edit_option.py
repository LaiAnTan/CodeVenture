import customtkinter as ctk

from ..ui_app import App
from ..ui_app_frame import App_Frame


class EditorWindow(App_Frame):

    """
    Frame class for displaying the main selection screen for educators.
    """

    def __init__(self):
        """
        Initialises the class.
        """

        super().__init__()
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure(0, weight=1)

        self.SetFrames()

    def refresh_variables(self):
        pass

    def attach_elements(self) -> None:
        """
        Performs attachment of frame elements onto the main frame.

        @return None
        """

        self.SetFrames()

    def SetFrames(self):
        """
        Setup the frame and elements.
        """

        self.header = ctk.CTkFrame(self)
        self.header.rowconfigure(0, weight=1)
        self.header.columnconfigure(0, weight=1)
        self.header.grid(row=0, column=0, sticky="s")

        self.content = ctk.CTkFrame(self)
        self.content.rowconfigure((0, 1), weight=1)
        self.content.columnconfigure(0, weight=1)
        self.content.grid(row=1, column=0, sticky="n")

        font = ctk.CTkFont(
            "Helvatica",
            size=24
        )

        bigtitle = ctk.CTkLabel(
            self.header,
            text="Create a New Activity Here",
            anchor=ctk.CENTER,
            font=font
        )
        bigtitle.grid(row=0, column=0, padx=50, pady=5)

        self.values = ['Module', 'Quiz', 'Challange']
        self.chosen = ctk.StringVar(value='Module')
        self.option_dropdown = ctk.CTkComboBox(
            self.content,
            values=self.values,
            variable=self.chosen,
            state='readonly'
        )
        self.option_dropdown.grid(row=0, column=0, padx=5, pady=5)

        new_ac = ctk.CTkButton(
            self.content,
            text="Create New Activity",
            command=self.newActivity
        )
        new_ac.grid(row=1, column=0, padx=5, pady=5)

        def logout_event():
            """
            Handles the logout event.
            """
            from ..ui_std_window_gen import loginPage
            loginPage()

        temp_log_out = ctk.CTkButton(
            self.content,
            text='Log Out',
            command=logout_event
        )
        temp_log_out.grid(row=2, column=0, padx=5, pady=5)

    # helper functions

    def newActivity(self):
        """
        Handles the event where a certain activity is chosen to be created.
        """
        option = self.chosen.get()
        print(f"{option} chosed")

        from ..ui_edu_window_gen import dispatcher
        dispatcher(option, None)


if __name__ == "__main__":
    App().change_frame(EditorWindow())
    App().mainloop()
