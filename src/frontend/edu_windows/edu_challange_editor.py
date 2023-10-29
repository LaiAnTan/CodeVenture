import customtkinter as ctk

from ...backend.activity.ac_classes.ac_activity import Activity

from ..ui_app import App
from .edu_activity_editor import ActivityEditor
from ...backend.activity.ac_classes.ac_challenge import Activity, Challange
from .helper_class.dataFileEditor import dataFileEditor
from .helper_class.solutionEntry import Modified_IDE
from .helper_class.ch_errorWindow import Ch_ErrorWindow
from .helper_class.testcaseEditor import testCaseEditor
from ...backend.factory.ChallengeFactory import ChallengeFactory

class ChallangeEditor(ActivityEditor):
    def __init__(self, existing_module: Challange = None):
        super().__init__(Activity.AType['Challenge'], existing_module)
        self.asset = []
        self.SetFrames()

    def ContentData(self):
        self.content_data.rowconfigure(1, weight=1)
        self.content_data.columnconfigure(0, weight=1)

        self.screen_var = ctk.StringVar(value = 'Challange Question Prompt')
        segmented_button = ctk.CTkSegmentedButton(
            self.content_data,
            values=['Challange Question Prompt', 'Solution', 'Hints', 'Test Cases'],
            variable=self.screen_var,
            dynamic_resizing=False,
            command=self.switch
        )
        segmented_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.now_displaying = ctk.CTkFrame(self.content_data, fg_color='transparent')
        self.now_displaying.columnconfigure(0, weight=1)
        self.now_displaying.rowconfigure(0, weight=1)
        self.now_displaying.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.init_all_frames()
        self.display_PromptEditor()

    def switch(self, placholder):
        match self.screen_var.get():
            case 'Challange Question Prompt':
                self.display_PromptEditor()
            case 'Solution':
                self.display_solution()
            case 'Hints':
                self.display_hints()
            case 'Test Cases':
                self.display_testcases()

    def init_all_frames(self):
        self.prompt = dataFileEditor(
            self.now_displaying,
            self.asset
        )

        self.solution = Modified_IDE(
            self.now_displaying,
        )

        self.hints = dataFileEditor(
            self.now_displaying,
            self.asset
        )

        self.testcase = testCaseEditor(
            self.now_displaying,
            self
        )

    def display_PromptEditor(self):
        for children in self.now_displaying.winfo_children():
            children.grid_forget()
        self.prompt.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def display_solution(self):
        for children in self.now_displaying.winfo_children():
            children.grid_forget()
        self.solution.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def display_hints(self):
        for children in self.now_displaying.winfo_children():
            children.grid_forget()
        self.hints.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def display_testcases(self):
        for children in self.now_displaying.winfo_children():
            children.grid_forget()
        self.testcase.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def GetContentData(self):
        return (
            self.prompt.get_content_data(),
            self.solution.get_content(),
            self.hints.get_content_data(),
            self.testcase.get_content_data()
        )

    def get_error_list(self):
        return (
            self.prompt.get_error_list(),
            self.solution.get_error(),
            self.hints.get_error_list(),
            self.testcase.get_error_list()
        )

    def ExportData(self):
        print("LOG: Exporting Challange...")

        error = self.get_error_list()
        content = self.GetContentData()

        if content[0] == []:
            error[0].append(('Prompt', 'Empty Prompt'))
        if content[2] == []:
            error[2].append(('Hints', 'Empty Hints'))
        if content[3] == []:
            error[3].append(('Test Cases', 'No Test Cases'))

        if error != ([], [], [], []): # all empty
            error_window = Ch_ErrorWindow(self, 450, 550, error)
            self.winfo_toplevel().wait_window(error_window)
            return
 
        # print(content)
        ChallengeFactory(self.GetHeaderData(), content, self.asset).build()

        print("Export Complete!")

if __name__ == "__main__":
    App().change_frame(ChallangeEditor(None))
    App().mainloop()