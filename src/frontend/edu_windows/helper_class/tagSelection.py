import customtkinter as ctk

from customtkinter.windows.widgets.core_widget_classes.dropdown_menu import DropdownMenu

class TagSelection(ctk.CTkOptionMenu):
    def __init__(self, master):
        self.font = ctk.CTkFont(
            'Helvetica',
            size=15
        )

        super().__init__(master, values=['Select Tags'])

        self.selected_tags = []
        self.tag_variable = {}
        self.init_tag_checkboxes()


    def init_tag_checkboxes(self):
        from ....backend.database.database_activity import ActivityDB

        tag_list = ActivityDB().getAllowedTags()
        for tag in tag_list:
            tag_var = ctk.BooleanVar(value=False)
            self.tag_variable[tag] = tag_var
            self._dropdown_menu.add_checkbutton(label=f'{tag}', 
                                                command=lambda x=tag: 
                                                self.set(x), 
                                                onvalue=1, 
                                                offvalue=0, 
                                                variable=tag_var,
                                                font=self.font,
                                                selectcolor='#3DCBC7'
                                                )


    def set(self, tag):
        if tag in self.selected_tags:
            self.selected_tags.remove(tag)
        else:
            self.selected_tags.append(tag)
        self.set_display()
        self._open_dropdown_menu()


    def set_display(self):
        if self.selected_tags:
            format_string = str(self.selected_tags).replace('[', '').replace(']', '').replace('\'', '').replace(',', ', ')
            self._text_label.configure(text=f"{format_string}")
        else:
            self._text_label.configure(text='Select Tags')


    def get(self):
        return self.selected_tags


    def import_values(self, values):
        self.selected_tags = values
        for selected_tag in self.selected_tags:
            if self.tag_variable.get(selected_tag, None) is not None:
                self.tag_variable[selected_tag].set(True)
            else:
                print(f"LOG: Unkown Tag Found: {selected_tag}")
        self.set_display()

if __name__ == "__main__":
    from ...ui_app import App

    idk = TagSelection(App().main_frame)
    idk.grid(row=0, column=0)
    idk.import_values(['input/output', 'functions'])
    App().main_frame.grid(row=0, column=0)
    App().mainloop()