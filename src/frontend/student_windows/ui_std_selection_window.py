import customtkinter as ctk

import src.backend.database.database_activity as ab

from ..ui_app import App
from ...backend.activity.ac_classes.ac_activity import Activity
from ...backend.user.user_student import Student
from ...backend.activity.ac_database.db_ac_completed import ActivityDictionary

# u gotta be kidding me
# https://stackoverflow.com/questions/66662493/how-to-progress-to-next-window-in-tkinter


class SelectionScreen():

    def __init__(self, student, attach: App) -> None:
        self.student = student
        self.activity_database = ab.ActivityDB()
        self.root = attach

        # initializes Activity Database Dictionary (ADD)
        ActivityDictionary()

    def return_to_studentMenu(self):
        from ..ui_std_window_gen import studentMenuPage
        studentMenuPage(self.root, self.student)

    def attach_elements(self):
        header = ctk.CTkFrame(self.root.main_frame)
        header.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        header_label = ctk.CTkLabel(
            header,
            text="I Dont Know What To Put As Title"
        )
        header_label.pack(side="left", padx=5, pady=5)

        back_button = ctk.CTkButton(
            header,
            text="Back",
            command=self.return_to_studentMenu
        )
        back_button.pack(side="right", padx=5, pady=5)

        content = ctk.CTkFrame(self.root.main_frame, height=450)
        content.grid(row=1, column=0, padx=5, pady=5)

        side_selection_bar = ctk.CTkFrame(content)
        side_selection_bar.grid(row=0, column=0, padx=5, pady=5, sticky="ns")

        content_width = 650
        main_contents_bar = ctk.CTkScrollableFrame(content, height=450, width=content_width)
        main_contents_bar.grid(row=0, column=1, padx=5, pady=5)

        self.display_all_info(0, content_width, main_contents_bar)

        button_labels = ["All", "Module", "Quiz", "Challange"]
        button_functions = [
            lambda : self.display_all_info(0, content_width, main_contents_bar),
            lambda : self.display_all_info(Activity.AType.Module.value, content_width, main_contents_bar),
            lambda : self.display_all_info(Activity.AType.Quiz.value, content_width, main_contents_bar),
            lambda : self.display_all_info(Activity.AType.Challenge.value, content_width, main_contents_bar)
        ]

        for index, button_label in enumerate(button_labels):
            button = ctk.CTkButton(
                side_selection_bar,
                text=button_label,
                command=button_functions[index],
                width=50
            )
            button.grid(row=index, column=0, padx=5, pady=5, sticky="ew")

    def display_all_info(self, type, max_width, attach_to: ctk.CTkScrollableFrame) -> None:
        for widgets in attach_to.winfo_children():
            widgets.destroy()

        result = self.activity_database.getListID(type)
        for index, module in enumerate(result):
            ret = DataChunk(module, max_width - 30, self.root, self.student).generateChunk(attach_to)
            ret.grid(row=index, column=0, padx=5, pady=5, sticky="ew")

    def __beep_boop(self) -> None:
        print("Button Pressed!")


class DataChunk():
    def __init__(self, activity_id, width, root: App, student: Student):
        self.activity = activity_id
        self.widget_width = width
        self.root = root
        self.student = student

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
        id_label.grid(row=0, column=0, padx=5, pady=5)

        title_label = ctk.CTkLabel(
            header_frame,
            text=self.contents[ab.ActivityDB.field.title.value]
        )
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

        from ..ui_std_window_gen import dispatcher

        student_done = ActivityDictionary.getDatabase(self.activity).getStudentEntry(self.student.username) is not None

        run_button = ctk.CTkButton(
            content_frame,
            text="Review" if student_done else "Attempt",
            width=50,
            command=lambda: dispatcher(self.id, self.type, self.root, self.student)
        )
        run_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        return ret_frame