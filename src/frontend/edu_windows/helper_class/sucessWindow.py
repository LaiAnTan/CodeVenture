import customtkinter as ctk

class successWindow(ctk.CTkToplevel):
    def __init__(self, master, user_action: str) -> None:
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
        new_button = ctk.CTkButton(
            self.buttonframes,
            text=label,
            command=lambda : self.attachment(function)
        )
        self.buttonframes.columnconfigure(len(self.buttonframes.winfo_children()), weight=1)
        new_button.grid(
            row=0,
            column=len(self.buttonframes.winfo_children()),
            padx=5,
            pady=5,
            sticky='nsew'
        )

    def attachment(self, function):
        function()
        self.destroy()

def hi():
    print('hi')

if __name__ == "__main__":
    from ...ui_app import App
    e = successWindow(App().main_frame, 'testing 123')
    e.add_a_action_button('hehe', hi)

    App().mainloop()