import src.backend.database.database_activity as ab
from ..ui_app_frame import App_Frame
from ...backend.activity.ac_functions import search_database
import customtkinter as ctk
from ..ui_edu_window_gen import dispatcher

class SelectionScreen(App_Frame):
    def __init__(self) -> None:
        super().__init__()

        self.activity_database = ab.ActivityDB()
        self.attach_elements()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

    def attach_elements(self):
        self.init_header()
        self.init_content()
        self.init_below_header()

    def refresh_variables(self):
        pass

    def init_header(self):
        header = ctk.CTkFrame(self)
        header.columnconfigure(0, weight=1)
        header.grid(row=0, column=0, sticky='ew')

        font = ctk.CTkFont(
            "Helvatica",
            size=24
        )

        very_obvious_label = ctk.CTkLabel(
            header,
            text='Activity Editor',
            font=font
        )
        very_obvious_label.grid(row=0, column=0, columnspan=2, sticky='ew')

        search_bar_frame = ctk.CTkFrame(
            header,
            fg_color='transparent',
            height=30
        )
        search_bar_frame.grid(
            row=1,
            column=0,
            sticky='ew'
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
            command=lambda: self.search_button_event(search_bar.get()),
            width=150,
        )

        search_button.grid(row=0,
                           column=1,
                           sticky="w",
                           padx=5,
                           pady=5)

        def logout_event():
            from ..ui_std_window_gen import loginPage
            loginPage()

        logout_button = ctk.CTkButton(
            header,
            text='Log Out',
            command=logout_event
        )
        logout_button.grid(row=1, column=1, padx=5, pady=5)


    def init_content(self):
        content = ctk.CTkFrame(self)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)
        content.grid(row=2, column=0, sticky='nsew')

        self.result_frame = ctk.CTkScrollableFrame(content)
        self.result_frame.grid(row=0, column=0, padx=5, pady=5, stick='nsew')
        self.result_frame.columnconfigure(0, weight=1)

        self.display_button_ids(self.activity_database.getListID(0))


    def init_below_header(self):
        below_header = ctk.CTkFrame(self)
        below_header.columnconfigure(0, weight=1)
        below_header.grid(row=1, column=0, sticky='ew')

        option_frame = ctk.CTkFrame(below_header)
        option_frame.columnconfigure(0, weight=1)
        option_frame.columnconfigure(1, weight=1)
        option_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.chosen = ctk.StringVar(value='Module')
        self.option_dropdown = ctk.CTkComboBox(
            option_frame,
            values=['Module', 'Quiz', 'Challenge'],
            variable=self.chosen,
            state='readonly',
            command=self.update_button,
            justify='center'
        )
        self.option_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.new_ac_button = ctk.CTkButton(
            option_frame,
            text="Create New Module",
            command=self.newActivity,
            width=540
        )
        self.new_ac_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')


    def search_button_event(self, query):
        self.result = search_database(query)

        ids = [res[0] for res in self.result]

        self.display_button_ids(ids)


    def display_button_ids(self, list_o_id):
        for children in self.result_frame.winfo_children():
            children.destroy()

        for index, id in enumerate(list_o_id):
            content = self.activity_database.retrieve_all_attr(id)
            
            id = content[self.activity_database.field.id.value]
            title = content[self.activity_database.field.title.value]

            button_frame = ctk.CTkFrame(
                self.result_frame
            )
            button_frame.columnconfigure(1, weight=1)
            button_frame.grid(row=index, column=0, padx=5, pady=5, sticky='nsew')

            id_displayer = ctk.CTkButton(
                button_frame,
                text=f'{id}',
                state='disabled',
                text_color_disabled='white',
                fg_color='#0E2347'
            )
            id_displayer.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

            button = ctk.CTkButton(
                button_frame,
                text=f'{title}',
                anchor='w',
                command=lambda x = id:self.editActivty(x)
            )
            button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    def editActivty(self, id):
        ac = activity_dispatcher(id)
        dispatcher(ac.type.name, ac)

    def newActivity(self):
        option = self.chosen.get()
        ac = dispatcher(option, None)

    def update_button(self, placeholder):
        self.new_ac_button.configure(text=f'Create New {self.chosen.get()}')


def activity_dispatcher(activityID):
    """
    Function that returns the correct Activity type based on stored value
    """

    from ...backend.database.database_activity import ActivityDB
    from ...backend.activity.ac_classes.ac_activity import Activity
    from ...backend.activity.ac_classes.ac_module import Module
    from ...backend.activity.ac_classes.ac_quiz import Quiz
    from ...backend.activity.ac_classes.ac_challenge import Challenge

    type_id = ActivityDB().fetch_attr(ActivityDB().field.type.name, activityID)
    type_name = Activity.AType(type_id).name
    match type_name:
        case 'Challenge':
            return Challenge(activityID)
        case 'Module':
            return Module(activityID)
        case 'Quiz':
            return Quiz(activityID)


if __name__ == "__main__":
    from ..ui_app import App
    App().change_frame(SelectionScreen())
    App().mainloop()