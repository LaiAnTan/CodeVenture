import customtkinter as ctk
from os import path, listdir

from .edu_activity_editor import ActivityEditor
from ...backend.activity.ac_classes.ac_activity import Activity
from ...backend.activity.ac_classes.ac_challenge import Activity, Challenge

class ChallangeEditor(ActivityEditor):

    """
    Frame class for displaying the challenge editor window for educators.
    """

    def __init__(self, existing_module: Challenge = None):
        """
        Initialises the class.
        """

        super().__init__(Activity.AType['Challenge'], existing_module)

        self.SetFrames()
        if self.editing:
            self.import_data()
    
    def import_data(self):
        solution_path = f'{self.ac.ModulePath}/solution'
        testcases_path = f'{self.ac.ModulePath}/testcase'
        data = []

        # get prompt
        for content in self.ac.content:
            type = content[0]
            value = content[1]
            match type:
                case Activity.Content_Type.Paragraph:
                    widget_type = 'paragraph'
                    widget_content = value
                case Activity.Content_Type.Code | Activity.Content_Type.Image:
                    widget_type = 'asset'
                    widget_content = self.ref_asset_dic[value]
            data.append((widget_type, widget_content))
        self.prompt.import_data_list(data)

        # get solution
        if path.exists(solution_path):
            with open(f'{solution_path}/main.py', 'r') as main_fd:
                code_in = ''.join(main_fd.readlines())
            with open(f'{solution_path}/input', 'r') as input_fd:
                input_in = ''.join(input_fd.readlines())
            self.solution.import_data((code_in, input_in))

        # get hints
        data.clear()
        for content in self.ac.hints.content:
            type = content[0]
            value = content[1]
            match type:
                case Activity.Content_Type.Paragraph:
                    widget_type = 'paragraph'
                    widget_content = value
                case Activity.Content_Type.Code | Activity.Content_Type.Image:
                    widget_type = 'asset'
                    widget_content = self.ref_asset_dic[value]
            data.append((widget_type, widget_content))
        self.hints.import_data_list(data)

        # get test_cases data
        data.clear()
        if path.exists(testcases_path):
            testcases = listdir(testcases_path)
            for testcase in testcases:
                with open(f'{testcases_path}/{testcase}') as tc_fd:
                    data.append(''.join(tc_fd.readlines()))
            self.testcase.import_data(data)


    def ContentData(self):
        """
        Add content data into frame.
        """
        self.content_data.rowconfigure(1, weight=1)
        self.content_data.columnconfigure(0, weight=1)

        self.screen_var = ctk.StringVar(value = 'Challenge Question Prompt')
        segmented_button = ctk.CTkSegmentedButton(
            self.content_data,
            values=['Challenge Question Prompt', 'Solution', 'Hints', 'Test Cases'],
            variable=self.screen_var,
            dynamic_resizing=False,
            command=self.switch
        )
        segmented_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.now_displaying = ctk.CTkFrame(self.content_data,
                                           fg_color='transparent')
        self.now_displaying.columnconfigure(0, weight=1)
        self.now_displaying.rowconfigure(0, weight=1)
        self.now_displaying.grid(row=1, column=0, padx=5, pady=5,
                                 sticky='nsew')

        self.init_all_frames()
        self.display_PromptEditor()

    def switch(self, placholder):
        """
        Switcher for handling different button events.
        """

        match self.screen_var.get():
            case 'Challenge Question Prompt':
                self.display_PromptEditor()
            case 'Solution':
                self.display_solution()
            case 'Hints':
                self.display_hints()
            case 'Test Cases':
                self.display_testcases()

    def init_all_frames(self):
        """
        Initialise all frames:
        - prompt
        - solution
        - hints
        - testcases
        """

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
        """
        Displays the prompt.
        """

        for children in self.now_displaying.winfo_children():
            children.grid_forget()
        self.prompt.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def display_solution(self):
        """
        Displays the solution.
        """

        for children in self.now_displaying.winfo_children():
            children.grid_forget()
        self.solution.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def display_hints(self):
        """
        Displays the hints.
        """

        for children in self.now_displaying.winfo_children():
            children.grid_forget()
        self.hints.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def display_testcases(self):
        """
        Displays the testcases.
        """

        for children in self.now_displaying.winfo_children():
            children.grid_forget()
        self.testcase.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def GetContentData(self):
        """
        Getter for content data.
        """

        return (
            self.prompt.get_content_data(),
            self.solution.get_content(),
            self.hints.get_content_data(),
            self.testcase.get_content_data()
        )

    def get_error_list(self):
        """
        Getter for error list.
        """

        header_error = self.get_header_errors()
        return (
            [header_error] if header_error[1] else [],
            self.prompt.get_error_list(),
            self.solution.get_error(),
            self.hints.get_error_list(),
            self.testcase.get_error_list()
        )

    def ExportData(self):
        print("LOG: Exporting Challenge...")

        error = self.get_error_list()
        content = self.GetContentData()

        if error != ([], [], [], [], []): # all empty
            error_window = Ch_ErrorWindow(self, 450, 550, error)
            self.winfo_toplevel().wait_window(error_window)
            return False

        ChallengeFactory(self.GetHeaderData(), content, self.asset).build()

        print("Export Complete!")
        return True


if __name__ == "__main__":
    App().change_frame(ChallengeEditor(None))
    App().mainloop()
