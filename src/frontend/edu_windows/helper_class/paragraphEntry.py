import customtkinter as ctk
from .entryForm import EntryForm
from _tkinter import TclError

class ParagraphEntryForm(EntryForm):
    def __init__(self, master, main_editor):
        super().__init__(master, main_editor)
        self.type = "paragraph"

        self.error = False
        self.error_msg = ''

        self.SetFrames()

    def SetContentFrame(self):
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)
        self.ContentEntryForm = ctk.CTkTextbox(
            self.content,
            height=150,
            wrap="word"
        )
        self.set_focus_widget(self.ContentEntryForm)

        self.setContentFormEvent()
        self.ContentEntryForm.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
    
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

    def RemoveSelf(self, placeholder=None):
        if not self.peek():
            self.delete_self(False)

    def goNextChunk(self, placeholder=None, content=None):
        # get self index
        self_index = self.get_index_instance()

        if content is None:
            # grab content of current chunk
            extracted_data = self.ContentEntryForm.get(ctk.INSERT, ctk.END).strip()
            self.ContentEntryForm.delete(ctk.INSERT, ctk.END)
        else:
            extracted_data = content

        next_index = self.getNextSimilarType()
        # check next one
        if next_index != -1 and next_index == self_index + 1:
            next_chunk = self.parent_frame.get_subframe(next_index)
            # next chunk is empty, just use this one
            if not next_chunk.peek():
                next_chunk.insertData(extracted_data)
                next_chunk.focus()
                self.parent_frame.scroll_frame(next_index / self.parent_frame.get_tracking_no())
                return "break"

        return self.makeNewInstance(self_index + 1, extracted_data)

    def makeNewInstance(self, where, content):
        new = ParagraphEntryForm(
            self.parent_frame,
            self.main_editor,
        )
        new.insertData(content)
        new.focus()
        self.parent_frame.add_element_specific(where, new)
        self.parent_frame.refresh_elements()
        self.parent_frame.scroll_frame(where / self.parent_frame.get_tracking_no())
        return "break"

    def PasteData(self, placeholder=None):
        try:
            value = self.winfo_toplevel().clipboard_get().strip()
        except TclError:
            print("LOG: clipboard is empty")
            return "break"

        first = 1
        current_index = self.get_index_instance()
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
                current_chunk = self.parent_frame.get_subframe(current_index)

        current_chunk.focus()
        return "break"
