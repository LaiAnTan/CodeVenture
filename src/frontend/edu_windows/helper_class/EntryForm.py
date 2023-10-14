import customtkinter as ctk
from abc import ABC, abstractmethod


class EntryForm(ctk.CTkFrame):
    def __init__(self, master, parent, height, width):
        super().__init__(master=master, height=height, width=width)

        self.type = "base"
        self.parent = parent
        self.height = height
        self.width = width

        self.rowconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self, width, height=15)
        self.header.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        self.content = ctk.CTkFrame(self, width, height=height - 15)
        self.content.grid(row=1, column=0, padx=5, pady=5)

        ## the main place to input data
        ## for paragraph, the textbox
        ## for image, the entry for file directory
        ## for code, uhh idk i think about it later
        self.ContentEntryForm = None

    def SetFrames(self):
        """Builds both Header and Content Frame"""
        self.SetHeader()
        self.SetContent()

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
        self.parent.content_frames.remove(self)
        self.grid_forget()

        match self.type:
            case "image":
                self.parent.imagecount -= 1
            case "code":
                self.parent.codecount -= 1

        try:
            self.parent.content_frames[-1].ContentEntryForm.focus()
        except IndexError:
            self.parent.focus()

    @abstractmethod
    def SetContent(self):
        pass

    def getNextSimilarType(self):
        self_index = self.parent.content_frames.index(self)
        for x, frames in enumerate(self.parent.content_frames[self_index + 1:]):
            if frames.type == self.type:
                return (self_index + 1) + x
        return -1