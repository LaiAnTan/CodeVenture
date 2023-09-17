import customtkinter as ctk

from ac_app import App
from ac_activity import Activity
import database.database_activity as ab

# u gotta be kidding me
# https://stackoverflow.com/questions/66662493/how-to-progress-to-next-window-in-tkinter

class SelectionScreen():
    activity_database = ab.ActivityDB()

    @classmethod
    def back_button_placeholder(cls):
        print("A Back Button that leads you back")
        print("In this case, it does nothing")
    
    @classmethod
    def attach_elements(cls, attach: App):
        cls.root = attach

        header = ctk.CTkFrame(attach.main_frame)
        header.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        header_label = ctk.CTkLabel(
            header,
            text="I Dont Know What To Put As Title"
        )

        back_button = ctk.CTkButton(
            header,
            text="Back",
            command=cls.back_button_placeholder
        )

        header_label.pack(side="left", padx=5, pady=5)
        back_button.pack(side="right", padx=5, pady=5)

        content = ctk.CTkFrame(attach.main_frame, height=450)
        content.grid(row=1, column=0, padx=5, pady=5)
        
        side_selection_bar = ctk.CTkFrame(content)
        side_selection_bar.grid(row=0, column=0, padx=5, pady=5, sticky="ns")

        content_width = 650
        main_contents_bar = ctk.CTkScrollableFrame(content, height=450, width=content_width)
        main_contents_bar.grid(row=0, column=1, padx=5, pady=5)

        cls.display_all_info(0, content_width, main_contents_bar)

        ## im lazy
        button_labels = ["All", "Module", "Quiz", "Challange"]
        button_functions = [
            lambda : cls.display_all_info(0, content_width, main_contents_bar),
            lambda : cls.display_all_info(Activity.AType.Module.value, content_width, main_contents_bar),
            lambda : cls.display_all_info(Activity.AType.Quiz.value, content_width, main_contents_bar),
            lambda : cls.display_all_info(Activity.AType.Challenge.value, content_width, main_contents_bar)
        ]

        for index, button_label in enumerate(button_labels):
            button = ctk.CTkButton(
                side_selection_bar,
                text=button_label,
                command=button_functions[index],
                width=50
            )
            button.grid(row=index, column=0, padx=5, pady=5, sticky="ew")

    @classmethod
    def display_all_info(cls, type, max_width, attach_to: ctk.CTkScrollableFrame) -> None:
        for widgets in attach_to.winfo_children():
            widgets.destroy()

        result = cls.activity_database.get_list_of_id(type)
        for index, module in enumerate(result):
            ret = DataChunk(module, max_width - 30, cls.root).generateChunk(attach_to)
            ret.grid(row=index, column=0, padx=5, pady=5, sticky="ew")

    @classmethod
    def __beep_boop(cls) -> None:
        print("Button Pressed!")

class DataChunk():
    def __init__(self, activity_id, width, root: App):
        self.activity = activity_id
        self.widget_width = width
        self.root = root

    def GetData(self):
        database = ab.ActivityDB()
        self.contents = database.retrieve_all_attr(self.activity)
        self.id = self.contents[database.field.id.value]
        self.type = self.contents[database.field.type.value]

    def generateChunk(self, attach_main):
        self.GetData()

        ret_frame = ctk.CTkFrame(attach_main)
        header_frame = ctk.CTkFrame(ret_frame)
        header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # header_frame.rowconfigure(0, weight=1)
        # header_frame.columnconfigure(0, weight=1)

        id_label = ctk.CTkLabel(
            header_frame,
            text=self.contents[ab.ActivityDB.field.id.value]
        )
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=self.contents[ab.ActivityDB.field.title.value]
        )

        id_label.grid(row=0, column=0, padx=5, pady=5)
        title_label.grid(row=0, column=1, padx=5, pady=5)

        content_frame = ctk.CTkFrame(ret_frame)
        content_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        content_label = ctk.CTkLabel(
            content_frame,
            text=self.contents[ab.ActivityDB.field.description.value],
            width=self.widget_width - 10 - 50,
            wraplength=self.widget_width - 20 - 50,
            justify="left",
            anchor="w"
        )
        content_label.grid(row=0, column=0, padx=5, pady=5)

        from ac_window_gen import dispatcher

        run_button = ctk.CTkButton(
            content_frame,
            text="Run",
            width=50,
            command=lambda : dispatcher(self.id, self.type, self.root)
        )
        run_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        return ret_frame