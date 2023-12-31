import customtkinter as ctk

import src.backend.database.database_activity as ab

from ..ui_app import App
from ..ui_app_frame import App_Frame
from ...backend.activity.ac_classes.ac_activity import Activity
from ...backend.user.user_student import Student

from ...backend.activity.ac_database.db_ac_completed import ActivityDictionary

from ...backend.activity.ac_functions import search_database, \
    filter_by_difficulty, filter_by_tags, sort_results

from config import LIGHTMODE_GRAY, DARKMODE_GRAY, TAG_DIR

# u gotta be kidding me
# https://stackoverflow.com/questions/66662493/how-to-progress-to-next-window-in-tkinter


class SelectionScreen(App_Frame):

    """
    Frame class for displaying the selection window.
    """

    def __init__(self, student) -> None:
        """
        Initializes the class.
        """
        super().__init__()

        self.student = student
        self.activity_database = ab.ActivityDB()
        self.results = search_database("")

        self.attach_elements()

    def refresh_variables(self):
        """
        Function that resets the variables to default values.
        """
        self.results = search_database("")

    def return_to_studentMenu(self):
        """
        Function that handles the back to student menu event when the back
        button is pressed.
        """
        from ..ui_std_window_gen import studentMenuPage
        studentMenuPage(self.student)

    def attach_elements(self):
        """
        Function that performs attachment of elements onto the main
        frame.
        """

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        content_width = 650

        # header

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        header.rowconfigure(0, weight=1)
        header.columnconfigure(0, weight=1)

        # search bar

        search_bar_frame = ctk.CTkFrame(
            header,
            fg_color="transparent",
            height=30
        )

        search_bar_frame.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        search_bar_frame.rowconfigure(0, weight=1)
        search_bar_frame.columnconfigure(0, weight=1)

        search_bar = ctk.CTkEntry(
            search_bar_frame,
            # width=400,
            placeholder_text="Looking for something?",
            font=("Helvetica", 14),
            justify=ctk.LEFT,
        )

        search_bar.grid(row=0,
                        column=0,
                        sticky="ew",
                        padx=5,
                        pady=5)

        search_button = ctk.CTkButton(
            search_bar_frame,
            text="Search",
            command=lambda: self.search_button_event(search_bar.get(),
                                                     content_width,
                                                     main_contents_bar),
            width=50,
        )

        search_button.grid(row=0,
                           column=1,
                           sticky="w",
                           padx=5,
                           pady=5)

        # sort

        sort_label = ctk.CTkLabel(header, text="Sort by:",)
        sort_label.grid(row=0, column=2, padx=5, pady=5)

        sort_options = ctk.CTkOptionMenu(header,
                                         values=['Name', 'Difficulty'],
                                         width=120,
                                         command=lambda option:
                                         self.sort_dropdown_display_auxiliary
                                         (option, header, 4, content_width,
                                          main_contents_bar)
                                         )
        sort_options.grid(row=0, column=3, padx=5, pady=5)

        back_button = ctk.CTkButton(
            header,
            text="Back",
            command=self.return_to_studentMenu,
            width=50
        )

        back_button.grid(row=0,
                         column=5,
                         sticky="e",
                         padx=5,
                         pady=5)

        # content

        content = ctk.CTkFrame(self, height=450,
                               fg_color="transparent")
        content.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        content.rowconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)

        side_selection_bar = ctk.CTkFrame(content, width=100)
        side_selection_bar.grid(row=0, column=0, padx=5, pady=5, sticky="nsw")

        main_contents_bar = ctk.CTkScrollableFrame(content,
                                                   height=450,
                                                   width=content_width)
        main_contents_bar.columnconfigure(0, weight=1)
        main_contents_bar.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.display_all_info(0, content_width, main_contents_bar)

        # filter frame in sidebar

        filter_frame = ctk.CTkFrame(side_selection_bar, width=100,
                                    fg_color="transparent")
        filter_frame.grid(row=0, column=0, padx=5, pady=5)

        filter_label = ctk.CTkLabel(filter_frame,
                                    text="Filter by:")
        filter_label.grid(row=0, column=0, padx=5, pady=5)

        filter_option = ctk.CTkOptionMenu(filter_frame,
                                          values=["difficulty", "tags",
                                                  "type"],
                                          command=lambda option: self
                                          .filter_dropdown_event
                                          (option, filter_content,
                                           content_width,
                                           main_contents_bar)
                                          )
        filter_option.grid(row=1, column=0, padx=5, pady=5)

        filter_content = ctk.CTkFrame(side_selection_bar, width=100,
                                      fg_color="transparent")
        filter_content.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        filter_content.columnconfigure(0, weight=1)

    def display_using_ids(self, ids: list[str], max_width, attach_to) -> None:
        """
        Function that creates activity tiles based on their id's and displays
        them in order.
        """

        # destroys previous widgets
        for widgets in attach_to.winfo_children():
            widgets.destroy()

        for index, module in enumerate(ids):
            dc = DataChunk(attach_to, module, max_width - 40,
                           self.student)
            dc.grid(row=index, column=0, padx=5, pady=5, sticky="ew")

    def display_all_info(self, type, max_width,
                         attach_to: ctk.CTkScrollableFrame) -> None:
        """
        Function that displays all activities that are currently in the
        database as activity tiles.
        """
        for widgets in attach_to.winfo_children():
            widgets.destroy()

        result = self.activity_database.getListID(type)

        self.display_using_ids(result, max_width, attach_to)

    def search_button_event(self, query, max_width,
                            attach_to: ctk.CTkScrollableFrame) -> None:
        """
        Handles the event when search button is pressed.
        """
        # runs the search function
        self.results = search_database(query)

        ids = [res[0] for res in self.results]

        self.display_using_ids(ids, max_width, attach_to)

    def sort_dropdown_display_auxiliary(self, option, attach_to, col,
                                        content_width, main_contents_bar):
        """
        Handles the event where an option from the main sort dropdown menu
        is chosen to display the auxiliary dropdown menu.
        """
        v = []

        match option.lower():
            case "difficulty":
                v = ["Low to High", "High to low"]
            case "name":
                v = ["A to Z", "Z to A"]

        def aux_sort_event(value):

            match value.lower():

                case "low to high":
                    self.results = sort_results(self.results, "difficulty",
                                                "asc")
                case "high to low":
                    self.results = sort_results(self.results, "difficulty",
                                                "desc")
                case "a to z":
                    self.results = sort_results(self.results, "name",
                                                "asc")
                case "z to a":
                    self.results = sort_results(self.results, "name",
                                                "desc")

            ids = [res[0] for res in self.results]

            self.display_using_ids(ids, content_width, main_contents_bar)

        aux_sort = ctk.CTkOptionMenu(attach_to,
                                     values=v,
                                     command=lambda x: aux_sort_event(x),
                                     width=120)
        aux_sort.grid(row=0, column=col, padx=5, pady=5)

    def filter_dropdown_event(self, option, attach_to, content_width,
                              main_contents_bar) -> None:
        """
        Handles the event where an option from the dropdown menu is chosen.
        """

        # destroys previous widgets
        for widgets in attach_to.winfo_children():
            widgets.destroy()

        # based on the option we will show different widgets
        match option:

            case "difficulty":

                # entry for max and min diff
                def diff_filter():

                    try:
                        max = int(max_diff.get())
                        min = int(min_diff.get())
                        if min > max:
                            return
                    except ValueError:
                        return

                    filtered = filter_by_difficulty(self.results, max, min)

                    ids = [item[0] for item in filtered]

                    self.display_using_ids(ids, content_width,
                                           main_contents_bar)

                attach_to.columnconfigure((0, 1, 2), weight=1)

                label = ctk.CTkLabel(attach_to, text="Difficulty Range")
                label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

                def callback(entry):
                    if str.isdigit(entry) or entry in ["", "Min", "Max"]:
                        return True
                    else:
                        return False

                # command to validate contents of textbox
                vcmd = (self.register(callback))

                # validate option: choose what to validate
                # validatecommand: what happens to validate
                # https://www.tcl.tk/man/tcl8.5/TkCmd/entry.html#M-validate
                min_diff = ctk.CTkEntry(attach_to,
                                        width=50,
                                        placeholder_text="Min",
                                        font=("Helvetica", 14),
                                        validate='all',
                                        validatecommand=(vcmd, '%P')
                                        )
                min_diff.grid(row=1, column=0, padx=(5, 0), pady=5)

                to_label = ctk.CTkLabel(attach_to, text="-")
                to_label.grid(row=1, column=1, padx=5, pady=5,)

                max_diff = ctk.CTkEntry(attach_to,
                                        width=50,
                                        placeholder_text="Max",
                                        font=("Helvetica", 14),
                                        validate='all',
                                        validatecommand=(vcmd, '%P')
                                        )
                max_diff.grid(row=1, column=2, padx=(0, 5), pady=5)

                apply_filter_button = ctk.CTkButton(attach_to,
                                                    text="Apply Filter",
                                                    command=diff_filter,
                                                    width=100,
                                                    anchor="center"
                                                    )
                apply_filter_button.grid(row=2, column=0,
                                         columnspan=3, padx=5, pady=5)

            case "tags":

                # checkboxes for tags
                with open(TAG_DIR, 'r') as file:
                    tag_labels = [line.strip('\n') for line in file]

                tag_states = [0] * len(tag_labels)

                def checkbox_filter(index):
                    tag_states[index] = 0 if tag_states[index] == 1 else 1

                    filtered = filter_by_tags(self.results, tag_labels,
                                              tag_states)

                    ids = [item[0] for item in filtered]

                    self.display_using_ids(ids, content_width,
                                           main_contents_bar)

                for index, tag_label in enumerate(tag_labels):

                    tag = ctk.CTkCheckBox(attach_to,
                                          text=tag_label,
                                          command=lambda x=index:  # late bind
                                          checkbox_filter(x),
                                          width=100,
                                          )
                    tag.grid(row=index, column=0, columnspan=3, padx=5, pady=5)

            case "type":

                # sidebar type buttons (filter by type)

                button_labels = ["All", "Module", "Quiz", "Challenge"]
                button_functions = [
                    lambda: self.display_all_info(0, content_width,
                                                  main_contents_bar),
                    lambda: self.display_all_info(Activity.AType.Module.value,
                                                  content_width,
                                                  main_contents_bar),
                    lambda: self.display_all_info(Activity.AType.Quiz.value,
                                                  content_width,
                                                  main_contents_bar),
                    lambda: self.display_all_info(Activity.AType.Challenge
                                                  .value,
                                                  content_width,
                                                  main_contents_bar)
                ]

                for index, button_label in enumerate(button_labels):
                    button = ctk.CTkButton(
                        attach_to,
                        text=button_label,
                        command=button_functions[index],
                        width=100,
                        anchor="center"
                    )
                    button.grid(row=index, column=0, columnspan=3,
                                padx=5, pady=5)


class DataChunk(ctk.CTkFrame):

    """
    Class that represents an activity tile containing:
    - ID of activity
    - Name of activity
    - Description of activity
    - button to enter activity
    """

    def __init__(self, master, activity_id, width, student: Student):
        """
        Initialises the class.
        """

        super().__init__(master=master,
                         fg_color=LIGHTMODE_GRAY if App().settings
                         .getSettingValue("lightmode")
                         .lower() == "true" else DARKMODE_GRAY)

        self.activity = activity_id
        self.widget_width = width
        self.student = student

        self.generateChunk()

    def GetData(self):
        """
        Gets the relevant data through the activity database.
        """
        database = ab.ActivityDB()
        self.contents = database.retrieve_all_attr(self.activity)
        self.id = self.contents[database.field.id.value]
        self.type = self.contents[database.field.type.value]

    def generateChunk(self):
        """
        Generates the activity tile and attaches it to attach_main.
        """

        self.GetData()

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="ew")

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

        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")
        content_frame.columnconfigure(0, weight=1)

        content_label = ctk.CTkLabel(
            content_frame,
            text=self.contents[ab.ActivityDB.field.description.value],
            width=self.widget_width - 10 - 50,
            wraplength=self.widget_width - 20 - 50,
            justify="left",
            anchor="w"
        )
        content_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        from ..ui_std_window_gen import dispatcher

        student_done = ActivityDictionary().getDatabase(self.activity)\
            .getStudentEntry(self.student.username) is not None

        run_button = ctk.CTkButton(
            content_frame,
            text="Review" if student_done else "Attempt",
            width=50,
            command=lambda: dispatcher(self.id, self.type, self.student)
        )
        run_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")


if __name__ == "__main__":
    App()
    from ...backend.user.user_student import Student

    select_s = SelectionScreen(Student('teststd'))
    App().change_frame(select_s)
    App().mainloop()
