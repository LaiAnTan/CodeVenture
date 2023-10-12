import customtkinter as ctk
from ui_app import App
from .edu_activity_editor import ActivityEditor

from ...backend.activity.ac_classes.ac_module import Activity, Module

class ModuleEditor(ActivityEditor):
    def __init__(self, master: App, width, height, existing_module: Module=None):
        super().__init__(master, width, height, Activity.AType['Module'], existing_module)

        self.SetFrames()
    
    def ContentData(self):
        ContentHeader = ctk.CTkFrame(self.content_data)
        ContentHeader.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        add_button = ctk.CTkButton(
            ContentHeader,
            text="Add Paragraph"
        )
        add_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        self.chosen_para_type = ctk.StringVar(value='Paragraph')
        self.para_types = ['Paragraph', 'Picture', 'Code Snippet']
        add_options = ctk.CTkOptionMenu(
            ContentHeader,
            values=self.para_types,
            variable=self.chosen_para_type
        )
        add_options.pack(side=ctk.RIGHT)

        content_entry_frame = ctk.CTkScrollableFrame(
            self.content_data,
            width=self.content_width + 5,
            height=self.max_height - 120
        )
        content_entry_frame.grid(row=1, column=0, padx=5, pady=5)

if __name__ == "__main__":
    master = App()
    editwin = ModuleEditor(master, 700, 450, None)
    editwin.grid(row=0, column=0)

    master.main_frame.grid(row=0, column=0)
    master.mainloop()