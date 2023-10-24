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
from .helper_class.errorWindow import ErrorWindow
from .helper_class.refreshScrollFrame import RefreshableScrollableFrame

from ...backend.factory.ModuleFactory import ModuleFactory

class ModuleEditor(ActivityEditor):
    def __init__(self, width, height, existing_module: Module=None):
        super().__init__(width, height, Activity.AType['Module'], existing_module)

        self.assets = []
        self.SetFrames()

    def ContentData(self):
        self.content_data.rowconfigure(1, weight=1)
        self.content_data.columnconfigure(0, weight=1)
        ContentHeader = ctk.CTkFrame(self.content_data)
        ContentHeader.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        try:
            asset_folder_image = ctk.CTkImage(
                Image.open(f'{ASSET_FOLDER}/asset_folder.png')
            )
        except FileNotFoundError:
            asset_folder_image = None

        asset_button = ctk.CTkButton(
            ContentHeader,
            image=asset_folder_image,
            text='Assets',
            width=100,
            command=self.show_asset_window
        )
        asset_button.pack(side=ctk.LEFT, padx=5, pady=5)

        add_button = ctk.CTkButton(
            ContentHeader,
            text="Add Entry Form At the End!",
            width=220,
            command=lambda : self.AddEntryPoint()
        )
        add_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        self.chosen_para_type = ctk.StringVar(value='Paragraph')
        self.para_types = ['Paragraph', 'Asset']
        add_options = ctk.CTkOptionMenu(
            ContentHeader,
            values=self.para_types,
            variable=self.chosen_para_type
        )
        add_options.pack(side=ctk.RIGHT, padx=(5, 40), pady=5)

        option_label = ctk.CTkLabel(
            ContentHeader,
            text='Type: ',
        )
        option_label.pack(side=ctk.RIGHT, padx=5, pady=5)

        self.entry_frame_height = self.content_data_height * 0.55
        self.content_frame = RefreshableScrollableFrame(
            self.content_data,
            # width=self.content_width + 5,
            # height=self.entry_frame_height
        )
        self.content_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nswe')

        self.entry_widget_heigth = self.entry_frame_height * 0.65
        self.entry_widget_width = self.content_width - 15

    ## helper functions

    def show_asset_window(self):
        asset_window = AssetWindow(self, 800, 700, self.assets)
        self.winfo_toplevel().wait_window(asset_window)

        # refresh all asset window
        self.refresh_asset_widgets()

    def refresh_asset_widgets(self):
        for content in self.content_frame.get_tracking_list():
            if isinstance(content, AssetPreview):
                content.refreshPreview()


    def AddEntryPoint(self) -> ParagraphEntryForm | AssetPreview:
        """Adds an certain type of entry form at the end of the window
        
        type is retrive from add_options CtkOptionMenu"""
        to_add = self.chosen_para_type.get()

        match to_add:
            case 'Paragraph':
                entry_form = ParagraphEntryForm(
                    self.content_frame,
                    self,
                    self.entry_widget_heigth,
                    self.entry_widget_width,
                )
            case 'Asset':
                entry_form = AssetPreview(
                    self.content_frame,
                    self,
                    self.entry_widget_width,
                    self.entry_widget_heigth,
                    self.assets
                )

        self.content_frame.track_element(entry_form)
        self.content_frame.refresh_elements()
        self.content_frame.scroll_frame(1)
        entry_form.focus()
        return entry_form

    def GetContentData(self):
        return [x.getData() for x in self.content_frame.get_tracking_list()]

    def get_error_list(self):
        error_status = [x.getError() for x in self.content_frame.get_tracking_list()]
        error_messages = []

        for index, error_ret in enumerate(error_status):
            if error_ret[0] is True:
                error_messages.append((index + 1, error_ret[1]))
        return error_messages

    def ExportData(self):
        print('LOG: Exporting...')

        error_messages = self.get_error_list()
        if error_messages:
            error_window = ErrorWindow(self, 450, 550, error_messages, 'export Module')
            self.winfo_toplevel().wait_window(error_window)
            return

        header = self.GetHeaderData()
        content = self.GetContentData()

        ModuleFactory(header, content, self.assets).build_Module()
        print('Export Complete!')

    def get_asset_list(self):
        return self.assets

if __name__ == "__main__":
    master = App()
    editwin = ModuleEditor(800, 650, None)
    editwin.grid(row=0, column=0, sticky='nsew')

    master.main_frame.grid(row=0, column=0, sticky='nswe')
    master.mainloop()