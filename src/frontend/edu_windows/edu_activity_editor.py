import customtkinter as ctk

from ..ui_app import App
from ..ui_app_frame import App_Frame
from ...backend.activity.ac_classes.ac_activity import Activity
from ...backend.database.database_activity import ActivityDB
from abc import abstractmethod, ABC
from .helper_class.confirmationWindow import ConfirmationWindow
from .helper_class.sucessWindow import successWindow
from .helper_class.tagSelection import TagSelection

from ...backend.activity.ac_classes.ac_challenge import Challenge


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

        self.id_variable = ctk.StringVar()
        self.name_variable = ctk.StringVar()
        self.difficulty_value = ctk.IntVar()

        # only used for editing
        self.ref_asset_dic = {}
        self.asset = self.get_correct_format_asset()

    # most probably not used since
    # theres no way you can
    # go back to this page
    # just re-init just in case
    def refresh_variables(self):
        self.id_variable.set(self.GetActivityID())
        self.name_variable.set(self.GetActivityName())
        self.difficulty_value.set(self.GetActivityDifficulty())

        self.ref_asset_dic = {}
        self.asset = self.get_correct_format_asset()

    def get_correct_format_asset(self):
        asset = []

        if self.editing is False:
            return asset

        self.format_image_chunks(self.ac, asset)
        self.format_code_chunks(self.ac, asset)

        # Challange has additional compiling for Hints
        if self.ac_type == Activity.AType.Challenge:
            self.ac: Challenge
            self.format_image_chunks(self.ac.hints, asset)
            self.format_code_chunks(self.ac.hints, asset)

        return asset

    def format_image_chunks(self, source, append_to):
        ac_dir = self.ac.ModulePath

        for id, value in source.img.items():
            # failsafe if file somehow has... multiple dot...
            name = '.'.join(value.split('.')[:-1])
            img_dir = f'{ac_dir}/{value}'
            asset_chunk = ('image', name, img_dir)
            if asset_chunk not in append_to:
                self.ref_asset_dic[id] = asset_chunk
                append_to.append(asset_chunk)

    def format_code_chunks(self, source, append_to):
        ac_dir = self.ac.ModulePath

        for id, value in source.code.items():
            full_dir = f'{ac_dir}/{value}'
            code_val = ''
            input_val = ''
            with open(f'{full_dir}/main.py', 'r') as code_fd:
                code_val = ''.join(code_fd.readlines())

            try:
                with open(f'{full_dir}/input', 'r') as input_fd:
                    input_val = ''.join(input_fd.readlines())
            except FileNotFoundError:  # code is NOT runnable
                input_val = None

            asset_chunk = ('code', value, code_val, input_val)

            if asset_chunk not in append_to:
                self.ref_asset_dic[id] = asset_chunk
                append_to.append(asset_chunk)

    @abstractmethod
    def import_data(self):
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
        second_row.columnconfigure(0, weight=30)
        second_row.columnconfigure(1, weight=70)
        second_row.grid(row=1, column=0, sticky="ew")

        difficulty_frame = ctk.CTkFrame(second_row, fg_color='transparent')
        difficulty_frame.columnconfigure(1, weight=1)
        difficulty_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        difficulty_label = ctk.CTkLabel(
            difficulty_frame,
            text=f"{self.ac_type_name}'s Difficulty: "
        )
        difficulty_label.grid(row=0, column=0, padx=5, pady=5)

        difficulty_slider = ctk.CTkSlider(
            difficulty_frame,
            from_=1,
            to=10,
            variable=self.difficulty_value,
            command=self.UpdateDifficultyLabel
        )
        difficulty_slider.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.difficulty_display = ctk.CTkLabel(
            difficulty_frame,
            text=self.difficulty_value.get()
        )
        self.difficulty_display.grid(row=0, column=2, padx=5, pady=5)

        tag_frame = ctk.CTkFrame(second_row, fg_color='transparent')
        tag_frame.columnconfigure(1, weight=1)
        tag_frame.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        tag_label = ctk.CTkLabel(
            tag_frame,
            text=f'{self.ac_type_name}\'s Tags'
        )
        tag_label.grid(row=0, column=0, padx=5, pady=5)

        self.tag_entry = TagSelection(
            tag_frame
        )
        self.tag_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

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
        self.SetActivtiyDescription()

        self.id_variable.set(self.GetActivityID())
        self.name_variable.set(self.GetActivityName())
        self.difficulty_value.set(self.GetActivityDifficulty())
        self.UpdateDifficultyLabel()

        if self.editing:
            self.tag_entry.import_values(self.ac.tag)

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
        from ..std_windows.ui_std_challenge_window import ChallengeWindow

        from ...backend.activity.ac_classes.ac_module import Module
        from ...backend.activity.ac_classes.ac_quiz import Quiz
        from ...backend.activity.ac_classes.ac_challenge import Challenge

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
                App().change_frame(ChallengeWindow(Challenge(ac_id), None,
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
            self.tag_entry.get(),
            self.description_entry.get("0.0", ctk.END)
        ]

    # helper function

    def UpdateDifficultyLabel(self):
        """
        Updates the difficulty label
        value is obtained through difficulty_value widget
        """

        self.difficulty_display.configure(text=self.difficulty_value.get())

    def SetActivtiyDescription(self):
        if self.editing:
            description = ActivityDB().fetch_attr(ActivityDB().field
                                                  .description.name,
                                                  self.ac.id)
        else:
            description = ''
        self.description_entry.insert('0.0', description)

    def GetActivityDifficulty(self):
        if self.editing:
            return self.ac.difficulty
        else:
            return 1

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

    def get_header_errors(self):
        error_list = []

        if self.name_variable.get().strip() == '':
            error_list.append('Name is Empty')
        if self.description_entry.get('0.0', ctk.END).strip() == '':
            error_list.append('No description for activity')
        if len(self.tag_entry.get()) == 0:
            error_list.append('Tag is not chosen for the activity')

        return ('Header', error_list)
