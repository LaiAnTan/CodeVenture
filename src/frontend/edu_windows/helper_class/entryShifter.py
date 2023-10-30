import customtkinter as ctk

from .refreshScrollFrame import RefreshableScrollableFrame, RSFWidget

class EntryShifterConfig(ctk.CTkFrame):
    """
    Class that implements the functionality that
    allows EntryForm objects to shift around the RSF
    onto RSFWidgets
    """

    def __init__(self,
                 master: RSFWidget,
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
        """
        Swaps the current widget position with the widget above it
        """
        index = self.master.get_index_instance()
        if index == 0:
            return
        self.parent.swap_order(index, index - 1)
        self.parent.scroll_frame((index) / self.parent.get_tracking_no())
        self.parent.refresh_elements()
        self.master.focus()

    def swap_down(self):
        """
        Swaps the current widget postiion with the widget below it
        """
        index = self.master.get_index_instance()
        if index == (self.parent.get_tracking_no() - 1):
            return
        self.parent.swap_order(index, index + 1)
        self.parent.scroll_frame((index) / self.parent.get_tracking_no())
        self.parent.refresh_elements()
        self.master.focus()
