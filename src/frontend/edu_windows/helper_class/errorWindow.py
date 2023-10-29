import customtkinter as ctk

class ErrorFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, width, error_list):
        super().__init__(master)
        self.columnconfigure(0, weight=1)

        if not error_list:
            all_goodframe = ctk.CTkFrame(self, fg_color='#00FF6F')
            all_goodframe.columnconfigure(0, weight=1)
            all_goodframe.grid(row=0, column=0, padx=5, pady=5, sticky='new')

            all_good_label = ctk.CTkLabel(
                all_goodframe,
                text='All Good!',
                text_color='black'
            )
            all_good_label.grid(row=0, column=0, padx=5, pady=5)
            return

        for index, error in enumerate(error_list):
            error_frame = ctk.CTkFrame(self, fg_color='#169398')
            error_frame.grid(row=index, column=0, padx=5, pady=5, sticky='new')

            error_frame.rowconfigure(0, weight=1)
            error_frame.columnconfigure(0, weight=1)

            error_location = ctk.CTkLabel(
                error_frame,
                text=f'Error in Entry {error[0]}',
                width=100,
                wraplength=90,
                fg_color='black',
                corner_radius=50
            )
            error_location.grid(row=0, column=0, padx=5, pady=5)

            error_message = ctk.CTkLabel(
                error_frame,
                text=f'{error[1]}',
                width = width - 100 - 85,
                wraplength = width - 15 - 100 - 85,
                justify='left'
            )
            error_message.grid(row=0, column=1, padx=5, pady=5, sticky='w')

class ErrorWindow(ctk.CTkToplevel):
    def __init__(self, master, width, height, error_list: list[str], user_action: str) -> None:
        super().__init__(master)
        self.geometry(f"{width}x{height}")
        self.title("Error!")

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        error_title = ctk.CTkLabel(
            self,
            text=f'{"Multiple errors" if len(error_list) > 1 else "An error was"} detected when attempting to {user_action}',
            wraplength= width - 15
        )
        error_title.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        errors = ErrorFrame(self, width, error_list)
        errors.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        okbutton = ctk.CTkButton(
            self,
            text='Ok',
            width=45,
            command=self.destroy,
            font=('Helvatica', 14)
        )
        okbutton.grid(row=2, column=0, padx=5, pady=5)

        self.wait_visibility()
        self.focus_set()
        self.grab_set()
