"""
Like Challenge Window

But for challenge editor
"""

import customtkinter as ctk
from .errorWindow import ErrorFrame

class Ch_ErrorWindow(ctk.CTkToplevel):
    def __init__(self, master, width, height, error_lists: tuple[list[str]]):
        super().__init__(master)
        self.geometry(f"{width}x{height}")
        self.title("Error!")

        self.widget_width = width 
        self.error_lists = error_lists

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        error_title = ctk.CTkLabel(
            self,
            text=f'Errors detected when attempting to export challenge activity',
            wraplength= width - 15
        )
        error_title.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.screen_var = ctk.StringVar(value = 'Challenge Question Prompt')
        segmented_button = ctk.CTkSegmentedButton(
            self,
            values=['Challenge Question Prompt', 'Solution', 'Hints', 'Test Cases'],
            variable=self.screen_var,
            dynamic_resizing=False,
            command=self.switch
        )
        segmented_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.init_frames()
        self.nowdisplaying = self.prompt_error # no effect, just stop it being None
        self.show_prompt_error()

    def init_frames(self):
        self.prompt_error = ErrorFrame(self, self.widget_width, self.error_lists[0])
        self.solution_error = ErrorFrame(self, self.widget_width, self.error_lists[1])
        self.hint_error = ErrorFrame(self, self.widget_width, self.error_lists[2])
        self.test_case_error = ErrorFrame(self, self.widget_width, self.error_lists[3])

    def switch(self, placeholder):
        match self.screen_var.get():
            case 'Challenge Question Prompt':
                self.show_prompt_error()
            case 'Solution':
                self.show_solution_error()
            case 'Hints':
                self.show_hint_error()
            case 'Test Cases':
                self.show_test_case_error()

    def show_prompt_error(self):
        self.nowdisplaying.grid_forget()

        self.nowdisplaying = self.prompt_error
        self.prompt_error.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

    def show_solution_error(self):
        self.nowdisplaying.grid_forget()

        self.nowdisplaying = self.solution_error
        self.solution_error.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

    def show_hint_error(self):
        self.nowdisplaying.grid_forget()

        self.nowdisplaying = self.hint_error
        self.hint_error.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

    def show_test_case_error(self):
        self.nowdisplaying.grid_forget()

        self.nowdisplaying = self.test_case_error
        self.test_case_error.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')