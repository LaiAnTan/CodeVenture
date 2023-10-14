import customtkinter as ctk
from ..ui_app import App
from ...backend.activity.ac_classes.ac_activity import Activity
from abc import abstractmethod, ABC

class ActivityEditor(ctk.CTkFrame, ABC):
    def __init__(self, master: App, width, height, type: Activity.AType, activity: Activity=None):
        super().__init__(master.main_frame, width=width, height=height)
        self.root = master

        self.ac = activity
        self.type = type
        self.editing = False
        self.type_name = type.name
        self.max_width = width
        self.max_height = height

        if activity is not None:
            self.editing = True
            self.type = self.ac.type

        header_height = 15
        self.header = ctk.CTkFrame(self, width=width, height=header_height)
        self.header.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.content_width = width
        self.content_height = height - header_height 
        self.content = ctk.CTkFrame(self, width=self.content_width, height=self.content_height)
        self.content.grid(row=1, column=0, padx=5, pady=5)

    def SetFrames(self):
        self.SetHeader()
        self.SetContent()

    def SetHeader(self):
        if self.editing:
            label_content = f"Now editing {self.ac.title}"
        else:
            label_content = f"Now creating a new {self.type.name}"

        label = ctk.CTkLabel(
            self.header,
            text=label_content
        )
        label.pack(side=ctk.LEFT, padx=5, pady=5)

        submit_button = ctk.CTkButton(
            self.header,
            text="Finish and Save"
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
            width=self.content_width
        )
        self.header_data.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.content_data = ctk.CTkFrame(
            self.content,
            width=self.content_width,
            height=420
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
            text=f"{self.type_name}'s ID: "
        )
        id_label.grid(row=0, column=0, padx=5, pady=5)

        id_entry = ctk.CTkEntry(
            first_row,
            width=120,
            placeholder_text=f"New {self.type_name} ID"
        )
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        title_label = ctk.CTkLabel(
            first_row,
            text=f"{self.type_name}'s Title: "
        )
        title_label.grid(row=0, column=2, padx=5, pady=5)

        title_entry = ctk.CTkEntry(
            first_row,
            width=420,
            placeholder_text="Title"
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
            text=f"{self.type_name}'s Difficulty: "
        )
        difficulty_label.grid(row=0, column=0, padx=5, pady=5)

        self.difficulty_value = ctk.IntVar(value=1)
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
            text=f'{self.type_name}\'s Tags'
        )
        tag_label.grid(row=0, column=3, padx=5, pady=5)

        tag_entry = ctk.CTkLabel(
            second_row,
            text="idk when is this getting implemented"
        )
        tag_entry.grid(row=0, column=4, padx=5, pady=5)

    @abstractmethod
    def ContentData(self):
        pass

    ## helper function

    def UpdateDifficultyLabel(self, value):
        self.difficulty_display.configure(text=self.difficulty_value.get())

# if __name__ == "__main__":
#     master = App()
#     editwin = ActivityEditor(master, 620, 450, Activity.AType['Module'])
#     editwin.grid(row=0, column=0)

#     master.main_frame.grid(row=0, column=0)
#     master.mainloop()