import customtkinter as ctk

class ConfirmationWindow(ctk.CTkToplevel):
    """
    A window that prompts user for confirmation for any action
    they want to take

    Displays the action that they are about to take and 
    prompts a yes and no button
    """
    def __init__(self, master, user_action: str) -> None:
        super().__init__(master)
        self.geometry("400x200")
        self.title("Are You Sure?")
        self.return_result = 0

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        warning_message = ctk.CTkLabel(
            self, 
            text=f"You are about to\n{user_action}\n\nAre You Sure?",
            font=('Helvetica', 18)
        )
        warning_message.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky='nswe')

        yesbutton = ctk.CTkButton(
            self,
            text="Yes",
            width=80,
            command=lambda : self.set_return_result(1),
            font=('Helvatica', 14)
        )
        yesbutton.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        nobutton = ctk.CTkButton(
            self,
            text="No",
            width=80,
            command=lambda : self.set_return_result(0),
            font=('Helvatica', 14)
        )
        nobutton.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        self.wait_visibility()
        self.focus_set()
        self.grab_set()

    def set_return_result(self, value):
        """
        Sets return result of the window

        then, destroys itself
        """
        self.return_result = value
        self.destroy()

    def get_value(self):
        """
        Get the return result of the window
        """
        return self.return_result