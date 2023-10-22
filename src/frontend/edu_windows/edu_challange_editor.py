import customtkinter as ctk

from ...backend.activity.ac_classes.ac_activity import Activity

from ..ui_app import App
from .edu_activity_editor import ActivityEditor
from ...backend.activity.ac_classes.ac_challenge import Activity, Challange

class ChallangeEditor(ActivityEditor):
    def __init__(self, width, height, existing_module: Activity = None):
        super().__init__(width, height, Activity.AType['Challenge'], existing_module)

        self.SetFrames()

    def ContentData(self):
        self.content_data.rowconfigure((0, 1), weight=1)
        self.content_data.columnconfigure(0, weight=1)

        self.screen_var = ctk.StringVar(value = 'Challange Question Prompt')
        segmented_button = ctk.CTkSegmentedButton(
            self.content_data,
            values=['Challange Question Prompt', 'Solution', 'Hints'],
            variable=self.screen_var,
            dynamic_resizing=False,
            command=self.switch
        )
        segmented_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    def switch(self, placholder):
        print(placholder)
        match self.screen_var.get():
            case 'Challange Question Prompt':
                raise NotImplementedError
            case 'Solution':
                raise NotImplementedError
            case 'Hints':
                raise NotImplementedError

    def GetContentData(self):
        pass

    def ExportData(self):
        raise NotImplemented

if __name__ == "__main__":
    master = App()
    editwin = ChallangeEditor(master, 800, 650, None)
    editwin.grid(row=0, column=0)

    master.main_frame.grid(row=0, column=0)
    master.mainloop()