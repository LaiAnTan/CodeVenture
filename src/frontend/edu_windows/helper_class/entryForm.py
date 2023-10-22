import customtkinter as ctk
from abc import ABC, abstractmethod
from .confirmationWindow import ConfirmationWindow
from .entryAdder import EntryAdder

class EntryForm(ctk.CTkFrame):
    def __init__(self, master, parent, height, width):
        super().__init__(master=master, height=height, width=width)

        self.master = master

        self.type = "base"
        self.parent = parent
        self.height = height
        self.width = width

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self, width, height=15)
        self.header.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.content = ctk.CTkFrame(self, width, height=height - 15)
        self.content.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        self.error = True
        self.error_msg = 'Entry Frame is left unused, Remove if not needed'

        ## the main place to input data
        self.ContentEntryForm = None

    def get_IndexInstance(self):
        """Returns which positon itself is in the parent's frame"""
        for index, x in enumerate(self.parent.content_frames):
            if x is self:
                return index
        return -1

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
            command= self.deleteSelf
        )
        remove_button.pack(side=ctk.RIGHT, padx=5, pady=5)

    def deleteSelf(self):
        """Remove ownself from parent
        - Sets focus to the next (or previous, if deleted one was the last element) Entry Frame
        - Scrolls the content frame to ensure focused entry is in frame"""
        confirmation = ConfirmationWindow(self.master, 'remove this entry form')
        self.master.winfo_toplevel().wait_window(confirmation)
        if confirmation.get_value() == 0:
            return

        next_index = self.parent.content_frames.index(self)
        self.parent.content_frames.remove(self)
        self.grid_forget()

        if self.parent.content_frames:
            scroll_to = next_index / len(self.parent.content_frames)
            if scroll_to >= 1:
                scroll_to = (next_index - 1) / (len(self.parent.content_frames) + 1)
        else:
            scroll_to = 0

        try:
            self.parent.content_frames[next_index].ContentEntryForm.focus()
        except IndexError:
            if self.parent.content_frames:
                self.parent.content_frames[-1].ContentEntryForm.focus()
            else:
                self.parent.focus()

        self.parent.ScrollContentFrame(scroll_to)

    @abstractmethod
    def SetContentFrame(self):
        pass

    @abstractmethod
    def getData(self):
        pass

    def SetEntryAdder(self):
        entry_adder = EntryAdder(self, self, self.parent, 45, self.width)
        entry_adder.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    def focus(self):
        self.ContentEntryForm.focus()

    def getNextSimilarType(self):
        self_index = self.parent.content_frames.index(self)
        for x, frames in enumerate(self.parent.content_frames[self_index + 1:]):
            if frames.type == self.type:
                return (self_index + 1) + x
        return -1
    
    def getError(self):
        return (
            self.error,
            self.error_msg
        )