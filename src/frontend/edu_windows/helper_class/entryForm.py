import customtkinter as ctk
from abc import ABC, abstractmethod
from .confirmationWindow import ConfirmationWindow
from .entryAdder import EntryAdder

from .refreshScrollFrame import RefreshableScrollableFrame
from .refreshScrollFrame import RSFWidget

class EntryForm(RSFWidget):
    def __init__(self, master: RefreshableScrollableFrame, main_editor, height, width):
        super().__init__(master=master, width=width, height=height)
        self.main_editor = main_editor

        self.type = "base"
        self.height = height
        self.width = width

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure(0, weight=1)

        entryform = ctk.CTkFrame(self)
        entryform.grid(row=1, column=0, sticky='ew')
        entryform.rowconfigure((0, 1), weight=1)
        entryform.columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(entryform)
        self.header.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.content = ctk.CTkFrame(entryform)
        self.content.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.error = True
        self.error_msg = 'Entry Frame is left unused, Remove if not needed'

        ## the main place to input data
        self.ContentEntryForm = None

    def SetFrames(self, no_entry_adder: bool = False):
        """Builds both Header and Content Frame"""
        self.SetHeader()
        self.SetContentFrame()

        if not no_entry_adder:
            self.SetEntryAdder()

    def SetHeader(self):
        cool_label = ctk.CTkLabel(
            self.header,
            text=f'{self.type.capitalize()} Entry Form',
            corner_radius=10,
        )
        cool_label.pack(side=ctk.LEFT)

        remove_button = ctk.CTkButton(
            self.header,
            text="Remove",
            command= self.delete_self
        )
        remove_button.pack(side=ctk.RIGHT, padx=5, pady=5)

    @abstractmethod
    def SetContentFrame(self):
        pass

    @abstractmethod
    def getData(self):
        pass

    def delete_self(self, confirm=True) -> None:
        if confirm:
            confirmation = ConfirmationWindow(self.master, 'remove this entry form')
            self.winfo_toplevel().wait_window(confirmation)
            if confirmation.get_value() == 0:
                return
        return super().delete_self()

    def SetEntryAdder(self):
        entry_adder = EntryAdder(self, 
                                 self.parent_frame, 
                                 self.main_editor, 
                                 45,
                                 self.width)
        entry_adder.grid(row=0, column=0, pady=5, sticky='ew')

    def getNextSimilarType(self):
        parent_tracking = self.parent_frame.get_tracking_list()
        self_index = parent_tracking.index(self)
        for x, frames in enumerate(parent_tracking[self_index + 1:]):
            if frames.type == self.type:
                return (self_index + 1) + x
        return -1

    def getError(self):
        return (
            self.error,
            self.error_msg
        )