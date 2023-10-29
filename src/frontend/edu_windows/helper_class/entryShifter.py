import customtkinter as ctk

from .refreshScrollFrame import RefreshableScrollableFrame, RSFWidget

class EntryShifterConfig(ctk.CTkFrame):
    """may god forgive me for what im about to do
    
    this widget allows EntryForm objects to shift around the RSF
    """

    def __init__(self,
                 master,
                 attached_form: RefreshableScrollableFrame, 
                 main_editor):
        # super().__init__(master, fg_color='#779DEB')

        self.master = master
        self.parent = attached_form
        self.main_editor = main_editor

        self.master.header.columnconfigure((0, 3), weight=10)
        bring_up = ctk.CTkButton(
            self.master.header,
            text='▲',
            width=0,
            command=self.swap_up
        )
        bring_up.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        bring_down = ctk.CTkButton(
            self.master.header,
            text='▼',
            width=0,
            command=self.swap_down
        )
        bring_down.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

    def swap_up(self):
        index = self.master.get_index_instance()
        if index == 0:
            return
        self.parent.swap_order(index, index - 1)
        self.parent.refresh_elements()

    def swap_down(self):
        index = self.master.get_index_instance()
        if index == (self.parent.get_tracking_no() - 1):
            return
        self.parent.swap_order(index, index + 1)
        self.parent.refresh_elements()

    def AddEntryPoint(self):
        """Adds an certain type of entry form in a certain position

        A direct copy of edu_module_editor's AddEntryPoint, it just works
        for the edu_module_editor instead

        God bless this spaghetti code"""
        index_to_add = self.master.get_index_instance()
        to_add = self.chosen_para_type.get()

        entry_form = self.main_editor.widget_factory(to_add)

        entry_form.focus()
        self.parent.add_element_specific(index_to_add, entry_form)
        self.parent.refresh_elements()
        self.parent.scroll_frame(index_to_add / self.parent.get_tracking_no())

if __name__ == "__main__":
    from ...ui_app import App
    a = App()

    test = EntryAdder(a.main_frame, a, 35, 700)
    test.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    a.main_frame.grid(row=0, column=0)
    a.mainloop()