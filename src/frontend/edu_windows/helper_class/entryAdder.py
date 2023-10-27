import customtkinter as ctk

from PIL import Image

from config import ASSET_FOLDER

from .refreshScrollFrame import RefreshableScrollableFrame, RSFWidget

class EntryAdder(ctk.CTkFrame):
    """may god forgive me for what im about to do
    
    this widget allows EntryForm objects to make a new instance in the main editor instance
    The new instance is placed ABOVE the object (there is a button to add at the bottom)"""
    def __init__(self,
                 master: RSFWidget,
                 attached_form: RefreshableScrollableFrame, 
                 main_editor):
        super().__init__(master)

        self.master = master
        self.parent = attached_form
        self.main_editor = main_editor
        self.columnconfigure((0, 1), weight=1)

        option_frame = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )
        option_frame.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        option_label = ctk.CTkLabel(
            option_frame,
            text='Type: ',
        )
        option_label.grid(row=0, column=0, padx=5, pady=5)

        self.chosen_para_type = ctk.StringVar(value='Paragraph')
        self.para_types = ['Paragraph', 'Asset']
        add_options = ctk.CTkOptionMenu(
            option_frame,
            values=self.para_types,
            variable=self.chosen_para_type
        )
        add_options.grid(row=0, column=1, padx=5, pady=5)

        add_button = ctk.CTkButton(
            self,
            text="Add An Entry Widget Above",
            command=lambda : self.AddEntryPoint()
        )
        add_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    def AddEntryPoint(self):
        """Adds an certain type of entry form in a certain position

        A direct copy of edu_module_editor's AddEntryPoint, it just works
        for the edu_module_editor instead

        God bless this spaghetti code"""
        from .paragraphEntry import ParagraphEntryForm
        from .assetPreview import AssetPreview

        index_to_add = self.master.get_index_instance()
        to_add = self.chosen_para_type.get()

        match to_add:
            case 'Paragraph':
                entry_form = ParagraphEntryForm(
                    self.parent,
                    self.main_editor,
                )
            case 'Asset':
                entry_form = AssetPreview(
                    self.parent,
                    self.main_editor,
                    self.main_editor.assets
                )

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