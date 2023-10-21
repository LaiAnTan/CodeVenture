import customtkinter as ctk

from ..ui_app import App
from ...backend.activity.ac_classes.ac_activity import Activity
from ...backend.database.database_activity import ActivityDB
from abc import abstractmethod, ABC

class ActivityEditor(ctk.CTkFrame, ABC):
    def __init__(self, master: App, width, height, type: Activity.AType, activity: Activity=None):
        super().__init__(master.main_frame, width=width, height=height)
        self.root = master

        self.ac = activity

        self.editing = False
        self.ac_type = type

        if activity is not None:
            self.editing = True
            self.ac_type = self.ac.type

        self.ac_type_name = type.name

        self.max_width = width
        self.max_height = height

        self.id_variable = ctk.StringVar(value=self.GetActivityID())
        self.name_variable = ctk.StringVar()
        self.difficulty_value = ctk.IntVar(value=1)

        header_height = 15
        self.header = ctk.CTkFrame(self, width=width, height=header_height)
        self.header.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.content_width = self.max_width
        self.content_height = self.max_height - header_height

        self.header_data_height = self.content_height * 0.30
        self.content_data_height = self.content_height * 0.70

        self.content = ctk.CTkFrame(self, width=self.content_width, height=self.content_height)
        self.content.grid(row=1, column=0, padx=5, pady=5)

    def SetFrames(self):
        self.SetHeader()
        self.SetContent()

    def SetHeader(self):
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
            command=self.ExportData
        )
        submit_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        back_button = ctk.CTkButton(
            self.header,
            text="Back"
        )
        back_button.pack(side=ctk.RIGHT, padx=5, pady=5)

    def SetContent(self):
        self.header_data = ctk.CTkFrame(
            self.content,
            width=self.content_width,
            height=self.header_data_height
        )
        self.header_data.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.content_data = ctk.CTkFrame(
            self.content,
            width=self.content_width,
            height=self.content_data_height
        )
        self.content_data.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.HeaderData()
        self.ContentData()

    def HeaderData(self):
        ## first row
        first_row = ctk.CTkFrame(
            self.header_data, 
            corner_radius=0
        )
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
            width=420,
            textvariable=self.name_variable
        )
        title_entry.grid(row=0, column=3, padx=5, pady=5)

        ## second row
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
        tag_entry.grid(row=0, column=4, padx=5, pady=5)

        ## third row
        thirdrow = ctk.CTkFrame(
            self.header_data,
            corner_radius=0
        )
        thirdrow.grid(row=2, column=0, sticky='ew')

        description_label = ctk.CTkLabel(
            thirdrow,
            text=f'{self.ac_type_name}\'s Description: '
        )
        description_label.grid(row=0, column=1, padx=5, pady=5, sticky='n')

        self.description_entry = ctk.CTkTextbox(
            thirdrow,
            width=self.content_width - 115,
            height=self.header_data_height * 0.3
        )
        self.description_entry.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

    @abstractmethod
    def ContentData(self):
        pass

    @abstractmethod
    def ExportData(self):
        pass

    @abstractmethod
    def GetContentData(self):
        pass

    def GetHeaderData(self):
        """Returns header data in the format of
        
        [id, type_num, name, difficulty_index, tags, description]"""
        return [
            "MD0001", # temporary, please remember to change
            # self.id_variable.get(),
            self.ac_type.value,
            self.name_variable.get(),
            self.difficulty_value.get(),
            ["py001", 'py002', 'py004'],
            self.description_entry.get("0.0", ctk.END)
        ]

    ## helper function

    def UpdateDifficultyLabel(self, value):
        self.difficulty_display.configure(text=self.difficulty_value.get())

    def GetActivityName(self):
        if self.editing:
            return self.ac.title
        else:
            return ''

    def GetActivityID(self):
        if self.editing:
            return self.ac.id
        else:
            return self.GetEmptyActivityID()

    def GetEmptyActivityID(self):
        """Gets the next empty ActivityID based on the list of ActivityIDs from the database
        Used for auto indexing activities"""
        id_list = ActivityDB().getListID(self.ac_type.value)

        # print(id_list)

        ## first 2 will be the type, last 3 is the value
        id_list = [int(x[2:]) for x in id_list]
        id_list.sort()
        ## search for closest empty spot
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