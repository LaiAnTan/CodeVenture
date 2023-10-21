import customtkinter as ctk
import os
from PIL import Image
from config import ASSET_FOLDER

from ..ui_app import App
from .edu_activity_editor import ActivityEditor
from ...backend.activity.ac_classes.ac_module import Activity, Module

from .helper_class.paragraphEntry import ParagraphEntryForm
from .helper_class.assetPreview import AssetPreview
from .helper_class.assetWindow import AssetWindow

from ...backend.factory.ModuleFactory import ModuleFactory

class ModuleEditor(ActivityEditor):
    def __init__(self, master: App, width, height, existing_module: Module=None):
        super().__init__(master, width, height, Activity.AType['Module'], existing_module)

        self.entry_height = self.content_data_height
        self.content_frames = []

        self.assets = []

        self.SetFrames()
    
    def ContentData(self):
        ContentHeader = ctk.CTkFrame(self.content_data)
        ContentHeader.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        add_button = ctk.CTkButton(
            ContentHeader,
            text="Add Entry Form",
            command=lambda : self.AddEntryPoint()
        )
        add_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        asset_button = ctk.CTkButton(
            ContentHeader,
            image=ctk.CTkImage(
                Image.open(f'{ASSET_FOLDER}/asset_folder.png')
            ),
            text='Assets',
            width=100,
            command=self.show_asset_window
        )
        asset_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        option_label = ctk.CTkLabel(
            ContentHeader,
            text='Type: ',
        )
        option_label.pack(side=ctk.LEFT, padx=5, pady=5)

        self.chosen_para_type = ctk.StringVar(value='Paragraph')
        self.para_types = ['Paragraph', 'Asset']
        add_options = ctk.CTkOptionMenu(
            ContentHeader,
            values=self.para_types,
            variable=self.chosen_para_type
        )
        add_options.pack(side=ctk.LEFT)

        index_label = ctk.CTkLabel(
            ContentHeader,
            text='Position: '
        )
        index_label.pack(side=ctk.LEFT, padx=(20, 0), pady=5)

        first_index = ctk.CTkButton(
            ContentHeader,
            text='First',
            command=lambda : self.index_value.set('1'),
            width=10
        )
        first_index.pack(side=ctk.LEFT, padx=5, pady=5)

        vcmd = self.register(lambda P : (str.isdigit(P) and int(P) < 1000 and int(P) > 0) or P == '')
        self.index_value = ctk.StringVar(value='1')
        index_entry = ctk.CTkEntry(
            ContentHeader,
            width=40,
            validate='key',
            validatecommand=(vcmd, '%P'),
            textvariable=self.index_value
        )
        index_entry.pack(side=ctk.LEFT, padx=5, pady=5)

        last_index = ctk.CTkButton(
            ContentHeader,
            text='Last',
            command=lambda : self.index_value.set(str(len(self.content_frames) + 1)),
            width=10
        )
        last_index.pack(side=ctk.LEFT, padx=5, pady=5)

        self.entry_frame_height = self.content_data_height * 0.55
        self.content_entry_frame = ctk.CTkScrollableFrame(
            self.content_data,
            width=self.content_width + 5,
            height=self.entry_frame_height
        )
        self.content_entry_frame.columnconfigure(0, weight=1)
        self.content_entry_frame.grid(row=1, column=0, padx=5, pady=5)

        self.entry_widget_heigth = self.entry_frame_height * 0.65
        self.entry_widget_width = self.content_width - 15


    ## helper functions

    def show_asset_window(self):
        asset_window = AssetWindow(self, 800, 700, self.assets)
        self.master.winfo_toplevel().wait_window(asset_window)

        # refresh all asset window
        for content in self.content_entry_frame.winfo_children():
            if isinstance(content, AssetPreview):
                content.refreshPreview()

    def AddEntryPoint(self):
        """Adds an certain type of entry form in a certain position
        
        type is retrive from add_options CtkOptionMenu
        index is retrive from index_entry CtkEntry"""
        if not self.index_value.get():
            self.index_value.set('1')
            return

        index = int(self.index_value.get()) - 1
        to_add = self.chosen_para_type.get()

        match to_add:
            case 'Paragraph':
                entry_form = ParagraphEntryForm(
                    self.content_entry_frame,
                    self,
                    self.entry_widget_heigth,
                    self.entry_widget_width,
                )
            case 'Asset':
                entry_form = AssetPreview(
                    self.content_entry_frame,
                    self,
                    self.entry_widget_width,
                    self.entry_widget_heigth,
                    self.assets
                )

        entry_form.ContentEntryForm.focus()
        if index >= len(self.content_frames):
            self.content_frames.append(entry_form)
        else:
            self.content_frames.insert(index, entry_form)

        self.Regrid_Components()
        self.ScrollContentFrame(index / len(self.content_frames))

    def ScrollContentFrame(self, how_much: float):
        """Processes all idle and pending task
        Scroll the frame until value stated in how_much is offscreen at the top"""

        self.content_entry_frame.update_idletasks()
        self.content_entry_frame._parent_canvas.yview_moveto(str(how_much))

    def Regrid_Components(self):
        """Remove all frame in container for entry frames
        Then, reattach them onto the frame

        Use when there are changes in the ordering of self.content_frames
        (removal or addition)"""
        for children in self.content_entry_frame.winfo_children():
            children.grid_forget()

        for index, components in enumerate(self.content_frames):
            self.content_entry_frame.rowconfigure(index, weight=1)
            components.grid(row=index, column=0, padx=5, pady=5, sticky='ew')

    def GetContentData(self):
        return [x.getData() for x in self.content_frames]

    def ExportData(self):
        print('LOG: Exporting...')
        header = self.GetHeaderData()
        content = self.GetContentData()

        ModuleFactory(header, content, self.assets).build_Module()
        print('Export Complete!')

if __name__ == "__main__":
    master = App()
    editwin = ModuleEditor(master, 800, 650, None)
    editwin.grid(row=0, column=0)

    master.main_frame.grid(row=0, column=0)
    master.mainloop()