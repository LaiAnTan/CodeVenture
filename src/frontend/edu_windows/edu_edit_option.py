import customtkinter as ctk
from ..ui_app import App
from .edu_module_editor import ModuleEditor

class EditorWindow(ctk.CTkFrame):
    def __init__(self):
        super().__init__(master.main_frame)
        
        self.rowconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self)
        self.header.rowconfigure(0, weight=1)
        self.header.columnconfigure(0, weight=1)
        self.header.grid(row=0, column=0, sticky="ew")

        self.content = ctk.CTkFrame(self)
        self.content.rowconfigure((0,1), weight=1)
        self.content.columnconfigure(0, weight=1)
        self.content.grid(row=1, column=0, sticky="ew")

        self.SetFrames()

    def SetFrames(self):
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

    ## helper functions

    def newActivity(self):
        option = self.chosen.get()
        print(f"{option} chosed")

        from ..ui_edu_window_gen import dispatcher
        dispatcher(option, None)

if __name__ == "__main__":
    master = App()
    editwin = EditorWindow(master)
    editwin.grid(row=0, column=0)
    master.main_frame.grid(row=0, column=0)
    master.mainloop()