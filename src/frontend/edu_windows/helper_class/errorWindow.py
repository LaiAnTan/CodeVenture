import customtkinter as ctk

class ErrorWindow(ctk.CTkToplevel):
    def __init__(self, master, width, height, error_list: list[str], user_action: str) -> None:
        super().__init__(master)
        self.geometry(f"{width}x{height}")
        self.title("Error!")
        self.return_result = 0

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        error_title = ctk.CTkLabel(
            self,
            text=f'{"Multiple errors" if len(error_list) > 1 else "An error was"} detected when attempting to {user_action}',
            wraplength= width - 15
        )
        error_title.grid(row=0, column=0, padx=5, pady=5)

        main_error_frame = ctk.CTkScrollableFrame(
            self,
            width=width,
            height=height - 95
        )
        main_error_frame.grid(row=1, column=0, padx=5, pady=5)

        for index, error in enumerate(error_list):
            error_frame = ctk.CTkFrame(main_error_frame, fg_color='#169398')
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

    def set_return_result(self, value):
        self.return_result = value
        self.destroy()

    def get_value(self):
        return self.return_result