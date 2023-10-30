import customtkinter as ctk


class successWindow(ctk.CTkToplevel):

    """
    Top level window to display success status.
    """

    def __init__(self, master, user_action: str) -> None:
        """
        Initialises the class.
        """

        super().__init__(master)
        self.geometry("400x200")
        self.title('Sucess')

        self.rowconfigure(0, weight=70)
        self.rowconfigure(1, weight=30)
        self.columnconfigure(0, weight=1)

        sucessmessage = ctk.CTkLabel(
            self,
            text=f'Sucessfully {user_action}',
            font=('Helvatica', 18),
            wraplength=400
        )
        sucessmessage.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.buttonframes = ctk.CTkFrame(self)
        self.buttonframes.rowconfigure(0, weight=1)
        self.buttonframes.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    def add_a_action_button(self, label, function) -> None:
        """
        Adds a button to the success top level window.
        """

        new_button = ctk.CTkButton(
            self.buttonframes,
            text=label,
            command=lambda: self.attachment(function)
        )
        self.buttonframes.columnconfigure(len(self.buttonframes
                                              .winfo_children()), weight=1)
        new_button.grid(
            row=0,
            column=len(self.buttonframes.winfo_children()),
            padx=5,
            pady=5,
            sticky='nsew'
        )

    def attachment(self, function):
        """
        Helper function to attach a function to lambda.
        """
        function()
        self.destroy()


if __name__ == "__main__":

    def hi():
        print('hi')

    from ...ui_app import App
    e = successWindow(App().main_frame, 'testing 123')
    e.add_a_action_button('hehe', hi)

    App().mainloop()
