import customtkinter as ctk
from abc import ABC, abstractmethod
from .confirmationWindow import ConfirmationWindow
from .entryShifter import EntryShifterConfig

from .refreshScrollFrame import RefreshableScrollableFrame
from .refreshScrollFrame import RSFWidget

class EntryForm(RSFWidget, ABC):
    """
    Abstract base class that handles all entry forms used in editor
    """
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
        """
        Builds the header in the widget
        """
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
        """
        Sets content of the widget

        Meant to be overriden
        """
        pass

    @abstractmethod
    def getData(self):
        """
        Function to get data contained in the widget

        Meant to be overriden
        """
        pass

    @abstractmethod
    def importData(self, data: tuple[str]):
        """
        Function to import data from a external source

        Meant to be overriden
        """
        pass

    def delete_self(self, confirm=True) -> None:
        """
        Function to remove itself from the parent frame

        Prompts user for confirmation to remove itself

        Runs delete_self function from RSFWidget

        The prompt is not shown if confirm is set to False
        """
        if confirm:
            confirmation = ConfirmationWindow(self.master, 'remove this entry form')
            self.winfo_toplevel().wait_window(confirmation)
            if confirmation.get_value() == 0:
                return
        return super().delete_self()

    def SetEntryAdder(self):
        """
        Sets the entry shifter for entry widget

        allows the entry to reposition itself in the frame
        """
        EntryShifterConfig(self,
                           self.parent_frame,
                           self.main_editor,
                           )

    def getNextSimilarType(self):
        """
        Gets the next similar type in the parent list
        """
        parent_tracking = self.parent_frame.get_tracking_list()
        self_index = parent_tracking.index(self)
        for x, frames in enumerate(parent_tracking[self_index + 1:]):
            if frames.type == self.type:
                return (self_index + 1) + x
        return -1

    @abstractmethod
    def getError(self):
        """
        Gets error within the widget

        meant to be overriden
        """
        pass