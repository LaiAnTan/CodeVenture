import customtkinter as ctk
from .EntryForm import EntryForm
from _tkinter import TclError

class ParagraphEntryForm(EntryForm):
    def __init__(self, master, parent, height, width):
        super().__init__(master, parent, height, width)
        self.type = "paragraph"
        self.SetFrames()

    def SetContentFrame(self):
        self.ContentEntryForm = ctk.CTkTextbox(
            self.content,
            height=self.height * 0.95,
            width=self.width - 15,
            wrap="word"
        )
        self.setContentFormEvent()
        self.ContentEntryForm.grid(row=0, column=0, padx=5, pady=5)
    
    def setContentFormEvent(self):
        self.ContentEntryForm.bind("<Return>", self.goNextChunk)
        self.ContentEntryForm.bind("<Control-KeyPress-v>", self.PasteData)
        self.ContentEntryForm.bind("<BackSpace>", self.RemoveSelf)

    def insertData(self, content):
        self.ContentEntryForm.insert(ctk.INSERT, content)

    def getData(self):
        """returns data input into the frame in the following format
        
        (type, data keyed into the paragraph)"""
        return (
            self.type,
            self.ContentEntryForm.get("0.0", ctk.END).strip()
        )

    def peek(self):
        """Check if there are content in the main entry form 

        Returns false if its empty"""
        return self.ContentEntryForm.get("0.0", ctk.END).strip() != ""

    ## helper functions

    def RemoveSelf(self, placeholder):
        if not self.peek():
            self.deleteSelf()

    def goNextChunk(self, placeholder, content=None):
        # get self index
        self_index = self.parent.content_frames.index(self)

        if content is None:
            # grab content of current chunk
            extracted_data = self.ContentEntryForm.get(ctk.INSERT, ctk.END).strip()
            self.ContentEntryForm.delete(ctk.INSERT, ctk.END)
        else:
            extracted_data = content

        next_index = self.getNextSimilarType()
        # check next one
        if next_index != -1 and next_index == self_index + 1:
            next_chunk: ParagraphEntryForm = self.parent.content_frames[next_index]
            # next chunk is empty, just use this one
            if next_chunk.peek():
                next_chunk.insertData(extracted_data)
                next_chunk.focus()
                self.parent.ScrollContentFrame(self_index / len(self.parent.content_frames))
                return "break"

        return self.makeNewInstance(self_index + 1, extracted_data)

    def makeNewInstance(self, where, content):
        new = ParagraphEntryForm(
            self.parent.content_entry_frame,
            self.parent,
            self.height,
            self.width,
        )
        self.parent.content_frames.insert(where, new)
        self.parent.Regrid_Components()
        new.insertData(content)
        new.ContentEntryForm.focus()
        self.parent.ScrollContentFrame((where) / len(self.parent.content_frames))
        return "break"
    
    def PasteData(self, placeholder):
        try:
            value = self.winfo_toplevel().clipboard_get().strip()
        except TclError:
            print("LOG: clipboard is empty")
            return "break"

        first = 1
        current_index = self.parent.content_frames.index(self)
        current_chunk = self
        for line in value.split('\n'):
            line = line.strip()
            if line == "":
                continue

            if first:
                current_chunk.insertData(line)
                first = 0
            else:
                current_chunk.goNextChunk(None, line.strip())
                current_index += 1
                current_chunk = self.parent.content_frames[current_index]

        current_chunk.ContentEntryForm.focus()
        return "break"
