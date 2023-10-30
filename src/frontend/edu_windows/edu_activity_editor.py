import customtkinter as ctk

from ..ui_app import App
from ..ui_app_frame import App_Frame
from ...backend.activity.ac_classes.ac_activity import Activity
from ...backend.database.database_activity import ActivityDB
from abc import abstractmethod, ABC
from .helper_class.confirmationWindow import ConfirmationWindow
from .helper_class.sucessWindow import successWindow


class ActivityEditor(App_Frame, ABC):

    """
    Abstract base class for displaying all types of activity editors.
    """

    def __init__(self, type: Activity.AType, activity: Activity = None):
        """
        Initialises the class.
        """

        super().__init__()
        self.ac = activity

        self.editing = False
        self.ac_type = type

        if activity is not None:
            self.editing = True
            self.ac_type = self.ac.type

        self.ac_type_name = type.name

        self.id_variable = ctk.StringVar(value=self.GetActivityID())
        self.name_variable = ctk.StringVar()
        self.difficulty_value = ctk.IntVar(value=1)

    def refresh_variables(self):
        pass

    def attach_elements(self) -> None:
        """
        Performs attachment of frame elements onto the main frame.

        @return None
        """

        self.SetFrames()

    def SetFrames(self):
        """
        Setup the frame and elements.
        """

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self)
        self.header.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=1, column=0, padx=5, pady=5, sticky='nswe')

        self.SetHeader()
        self.SetContent()

    def SetHeader(self):
        """
        Setup the frames in the header.
        """

        if self.editing:
            label_content = f"Now editing {self.ac.title}"
        else:
            label_content = f"Now creating a new {self.ac_type.name}"

        label = ctk.CTkLabel(
            self.header,
            text=label_content
        )
        label.pack(side=ctk.LEFT, padx=5, pady=5)

        submit_button = ctk.CTkButton(
            self.header,
            text="Finish and Export",
            command=self.PreExportData
        )
        submit_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        back_button = ctk.CTkButton(
            self.header,
            text="Back",
            command=lambda: App().go_back_history()
        )
        back_button.pack(side=ctk.RIGHT, padx=5, pady=5)

    def SetContent(self):
        """
        Setup the frames in content.
        """

        self.content.rowconfigure(1, weight=1)
        self.content.columnconfigure(0, weight=1)

        self.header_data = ctk.CTkFrame(
            self.content,
            fg_color='transparent'
        )
        self.header_data.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        self.content_data = ctk.CTkFrame(
            self.content
        )
        self.content_data.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.HeaderData()
        self.ContentData()

    def HeaderData(self):
        """
        Setup the elements in header.
        """

        self.header_data.rowconfigure((0, 1, 2), weight=1)
        self.header_data.columnconfigure(0, weight=1)

        # first row
        first_row = ctk.CTkFrame(
            self.header_data,
            corner_radius=0
        )
        first_row.rowconfigure(0, weight=1)
        first_row.columnconfigure(3, weight=1)
        first_row.grid(row=0, column=0, sticky="ew")

        id_label = ctk.CTkLabel(
            first_row,
            text=f"{self.ac_type_name}'s ID: "
        )
        id_label.grid(row=0, column=0, padx=5, pady=5)

        id_entry = ctk.CTkEntry(
            first_row,
            width=120,
            textvariable=self.id_variable,
            state=ctk.DISABLED
        )
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        title_label = ctk.CTkLabel(
            first_row,
            text=f"{self.ac_type_name}'s Title: "
        )
        title_label.grid(row=0, column=2, padx=5, pady=5)

        title_entry = ctk.CTkEntry(
            first_row,
            textvariable=self.name_variable
        )
        title_entry.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        # second row
        second_row = ctk.CTkFrame(
            self.header_data,
            corner_radius=0
        )
        second_row.grid(row=1, column=0, sticky="ew")

        difficulty_label = ctk.CTkLabel(
            second_row,
            text=f"{self.ac_type_name}'s Difficulty: "
        )
        difficulty_label.grid(row=0, column=0, padx=5, pady=5)

        difficulty_slider = ctk.CTkSlider(
            second_row,
            from_=1,
            to=10,
            variable=self.difficulty_value,
            command=self.UpdateDifficultyLabel
        )
        difficulty_slider.grid(row=0, column=1, padx=5, pady=5)

        self.difficulty_display = ctk.CTkLabel(
            second_row,
            text=self.difficulty_value.get()
        )
        self.difficulty_display.grid(row=0, column=2, padx=5, pady=5)

        tag_label = ctk.CTkLabel(
            second_row,
            text=f'{self.ac_type_name}\'s Tags'
        )
        tag_label.grid(row=0, column=3, padx=5, pady=5)

        tag_entry = ctk.CTkLabel(
            second_row,
            text="TODO: Implement Tag Choosing"
        )
        tag_entry.grid(row=0, column=4, padx=5, pady=5, sticky='ew')

        # third row
        thirdrow = ctk.CTkFrame(
            self.header_data,
            corner_radius=0
        )
        thirdrow.rowconfigure(0, weight=1)
        thirdrow.columnconfigure(1, weight=1)
        thirdrow.grid(row=2, column=0, sticky='sew')

        description_label = ctk.CTkLabel(
            thirdrow,
            text=f'{self.ac_type_name}\'s Description: '
        )
        description_label.grid(row=0, column=0, padx=5, pady=5, sticky='n')

        self.description_entry = ctk.CTkTextbox(
            thirdrow,
            height=65
        )
        self.description_entry.grid(row=0, column=1, padx=5, pady=5,
                                    sticky='ew')

    @abstractmethod
    def ContentData(self):
        pass

    def PreExportData(self):
        """
        Handles the event before data is to be exported.
        """

        confirm = ConfirmationWindow(self, f'export {self.ac_type_name}')
        self.winfo_toplevel().wait_window(confirm)
        if not confirm.get_value():
            return

        if self.ExportData():
            ok_win = successWindow(self, f'exported {self.ac_type_name} {self.id_variable.get()}')
            ok_win.add_a_action_button('Back To Selection',
                                       lambda: App().go_back_history())
            ok_win.add_a_action_button('Preview Window', self.preview_win)
            self.winfo_toplevel().wait_window(ok_win)

    def preview_win(self):
        """
        Handles the preview activity event.
        """

        from ..std_windows.ui_std_module_window import ModuleWindow
        from ..std_windows.ui_std_quiz_window import QuizWindow
        from ..std_windows.ui_std_challenge_window import ChallangeWindow

        from ...backend.activity.ac_classes.ac_module import Module
        from ...backend.activity.ac_classes.ac_quiz import Quiz
        from ...backend.activity.ac_classes.ac_challenge import Challange

        ac_id = self.id_variable.get()
        App().clean_frame()
        match self.ac_type:
            case Activity.AType.Module:
                App().change_frame(ModuleWindow(Module(ac_id), None, True),
                                   False)
            case Activity.AType.Quiz:
                App().change_frame(QuizWindow(Quiz(ac_id), None, True),
                                   False)
            case Activity.AType.Challenge:
                App().change_frame(ChallangeWindow(Challange(ac_id), None,
                                                   True), False)

    @abstractmethod
    def ExportData(self):
        pass

    @abstractmethod
    def GetContentData(self):
        pass

    def GetHeaderData(self):
        """
        Returns header data in the format of
        [id, type_num, name, difficulty_index, tags, description]
        """

        return [
            self.id_variable.get(),
            self.ac_type.value,
            self.name_variable.get(),
            self.difficulty_value.get(),
            ["py001", 'py002', 'py004'],
            self.description_entry.get("0.0", ctk.END)
        ]

    # helper function

    def UpdateDifficultyLabel(self, value):
        """
        Updates the difficulty label to (value)
        """

        self.difficulty_display.configure(text=self.difficulty_value.get())

    def GetActivityName(self):
        """
        Getter for activity name
        """

        if self.editing:
            return self.ac.title
        else:
            return ''

    def GetActivityID(self):
        """
        Getter for activity id
        """

        if self.editing:
            return self.ac.id
        else:
            return self.GetEmptyActivityID()

    def GetEmptyActivityID(self):
        """
        Gets the next empty ActivityID based on the list of ActivityIDs
        from the database

        Used for auto indexing activities
        """

        id_list = ActivityDB().getListID(self.ac_type.value)

        # first 2 will be the type, last 3 is the value
        id_list = [int(x[2:]) for x in id_list]
        id_list.sort()

        # search for closest empty spot
        index = len(id_list)
        for actual_index, ac_index in enumerate(id_list):
            if actual_index != ac_index:
                index = ac_index
                break
        return f'{self.ac_type.getSubScript()}{index:04d}'

# if __name__ == "__main__":
#     master = App()
#     editwin = ActivityEditor(master, 620, 450, Activity.AType['Module'])
#     editwin.grid(row=0, column=0)

#     master.main_frame.grid(row=0, column=0)
#     master.mainloop()
