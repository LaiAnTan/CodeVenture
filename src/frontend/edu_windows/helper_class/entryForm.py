import customtkinter as ctk
from abc import ABC, abstractmethod
from .confirmationWindow import ConfirmationWindow
from .entryAdder import EntryAdder
from .entryShifter import EntryShifterConfig

from .refreshScrollFrame import RefreshableScrollableFrame
from .refreshScrollFrame import RSFWidget

class EntryForm(RSFWidget, ABC):
    def __init__(self, master: RefreshableScrollableFrame, main_editor):
        super().__init__(master=master)
        self.main_editor = main_editor

        self.type = "base"

    def SetFrames(self, no_entry_adder: bool = False):
        """Builds both Header and Content Frame"""

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure(0, weight=1)

        if not no_entry_adder:
            entryform = ctk.CTkFrame(self, fg_color='#394764')
            entryform.grid(row=1, column=0, sticky='ew')
            entryform.rowconfigure((0, 1), weight=1)
            entryform.columnconfigure(0, weight=1)
        else:
            entryform = self
            entryform.configure(fg_color='#394764')

        self.header = ctk.CTkFrame(entryform, fg_color='transparent')
        self.header.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.content = ctk.CTkFrame(entryform, fg_color='transparent')
        self.content.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.SetHeader()
        self.SetContentFrame()

        if not no_entry_adder:
            self.SetEntryAdder()

    def SetHeader(self):
        self.header.columnconfigure((1, 2), weight=40)

        # theres a reason why these two are at 1 and 2...
        cool_label = ctk.CTkLabel(
            self.header,
            text=f'{self.type.capitalize()} Entry Form',
            corner_radius=10,
        )
        cool_label.grid(row=0, column=1, sticky='w')

        remove_button = ctk.CTkButton(
            self.header,
            text="Remove",
            command= self.delete_self
        )
        remove_button.grid(row=0, column=2, sticky='e')

    @abstractmethod
    def SetContentFrame(self):
        pass

    @abstractmethod
    def getData(self):
        pass

    @abstractmethod
    def importData(self, data: tuple[str]):
        self.error = False

    def delete_self(self, confirm=True) -> None:
        if confirm:
            confirmation = ConfirmationWindow(self.master, 'remove this entry form')
            self.winfo_toplevel().wait_window(confirmation)
            if confirmation.get_value() == 0:
                return
        return super().delete_self()

    def SetEntryAdder(self):
        EntryShifterConfig(self,
                           self.parent_frame,
                           self.main_editor,
                           )

    def getNextSimilarType(self):
        parent_tracking = self.parent_frame.get_tracking_list()
        self_index = parent_tracking.index(self)
        for x, frames in enumerate(parent_tracking[self_index + 1:]):
            if frames.type == self.type:
                return (self_index + 1) + x
        return -1

    @abstractmethod
    def getError(self):
        pass