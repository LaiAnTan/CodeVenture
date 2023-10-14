import customtkinter as ctk
from ..ui_app import App
from .edu_activity_editor import ActivityEditor

from .helper_class.imageEntry import ImageEntryForm
from .helper_class.paragraphEntry import ParagraphEntryForm
from .helper_class.codeEntry import CodeEntryForm
from ...backend.activity.ac_classes.ac_module import Activity, Module

class ModuleEditor(ActivityEditor):
    def __init__(self, master: App, width, height, existing_module: Module=None):
        super().__init__(master, width, height, Activity.AType['Module'], existing_module)
        self.imagecount = 0
        self.codecount = 0

        self.SetFrames()
    
    def ContentData(self):
        ContentHeader = ctk.CTkFrame(self.content_data)
        ContentHeader.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        add_button = ctk.CTkButton(
            ContentHeader,
            text="Add Paragraph",
            command=lambda : self.AddEntryPoint()
        )
        add_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        self.chosen_para_type = ctk.StringVar(value='Paragraph')
        self.para_types = ['Paragraph', 'Picture', 'Code Snippet']
        add_options = ctk.CTkOptionMenu(
            ContentHeader,
            values=self.para_types,
            variable=self.chosen_para_type
        )
        add_options.pack(side=ctk.RIGHT)

        self.content_frames: list[ParagraphEntryForm] = []
        self.content_entry_frame = ctk.CTkScrollableFrame(
            self.content_data,
            width=self.content_width + 5,
            height=self.max_height - 120
        )
        self.content_entry_frame.grid(row=1, column=0, padx=5, pady=5)
        self.content_frame_height = self.max_height - 320
        self.content_frame_width = self.content_width - 10

    def AddEntryPoint(self):
        to_add = self.chosen_para_type.get()

        match to_add:
            case 'Paragraph':
                entry_form = ParagraphEntryForm(
                    self.content_entry_frame,
                    self,
                    self.content_frame_height,
                    self.content_frame_width,
                )
            case 'Picture':
                entry_form = ImageEntryForm(
                    self.content_entry_frame,
                    self,
                    self.content_frame_height,
                    self.content_frame_width,
                )
                self.imagecount += 1
            case 'Code Snippet':
                entry_form = CodeEntryForm(
                    self.content_entry_frame,
                    self,
                    self.content_frame_height,
                    self.content_frame_width
                )
                self.codecount += 1

        # entry_form.ContentEntryForm.focus()
        self.content_frames.append(entry_form)

        self.Regrid_Components()
        self.ScrollContentFrame(1.0)

    def ScrollContentFrame(self, how_much: float):
        ## processes all idle and pending task
        ## in this case, adding the new widget onto the frame
        self.content_entry_frame.update_idletasks()

        ## scroll the frame
        ## note that how_much = how much of the percentage of the screen is 
        ## at the off_screen at the top
        self.content_entry_frame._parent_canvas.yview_moveto(str(how_much))

    def Regrid_Components(self):
        for children in self.content_entry_frame.winfo_children():
            children.grid_forget()
    
        for index, components in enumerate(self.content_frames):
            components.grid(row=index, column=0, padx=5, pady=5)


if __name__ == "__main__":
    master = App()
    editwin = ModuleEditor(master, 700, 450, None)
    editwin.grid(row=0, column=0)

    master.main_frame.grid(row=0, column=0)
    master.mainloop()