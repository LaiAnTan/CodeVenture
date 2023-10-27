import customtkinter as ctk

from .paragraphEntry import ParagraphEntryForm
from .assetPreview import AssetPreview
from .assetWindow import AssetWindow
from .errorWindow import ErrorWindow
from .refreshScrollFrame import RefreshableScrollableFrame
from PIL import Image
from config import ASSET_FOLDER

class dataFileEditor(ctk.CTkFrame):
    def __init__(self, master, asset_list):
        super().__init__(master=master, fg_color='transparent')
        self.assets = asset_list

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        try:
            asset_folder_image = ctk.CTkImage(
                Image.open(f'{ASSET_FOLDER}/asset_folder.png')
            )
        except FileNotFoundError:
            asset_folder_image = None

        asset_adder_frame = ctk.CTkFrame(
            self
        )
        asset_adder_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        asset_button = ctk.CTkButton(
            asset_adder_frame,
            image=asset_folder_image,
            text='Assets',
            width=100,
            command=self.show_asset_window
        )
        asset_button.pack(side=ctk.LEFT, padx=5, pady=5)

        add_button = ctk.CTkButton(
            asset_adder_frame,
            text="Add Entry Form At the End!",
            width=220,
            command=lambda : self.add_entry_point()
        )
        add_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        self.chosen_para_type = ctk.StringVar(value='Paragraph')
        self.para_types = ['Paragraph', 'Asset']
        add_options = ctk.CTkOptionMenu(
            asset_adder_frame,
            values=self.para_types,
            variable=self.chosen_para_type
        )
        add_options.pack(side=ctk.RIGHT, padx=(5, 40), pady=5)

        option_label = ctk.CTkLabel(
            asset_adder_frame,
            text='Type: ',
        )
        option_label.pack(side=ctk.RIGHT, padx=5, pady=5)

        self.content_frame = RefreshableScrollableFrame(
            self,
        )
        self.content_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nswe')

    def add_entry_point(self) -> ParagraphEntryForm | AssetWindow:
        """Adds an certain type of entry form at the end of the window
        
        type is retrive from add_options CtkOptionMenu"""
        to_add = self.chosen_para_type.get()

        match to_add:
            case 'Paragraph':
                entry_form = ParagraphEntryForm(
                    self.content_frame,
                    self,
                )
            case 'Asset':
                entry_form = AssetPreview(
                    self.content_frame,
                    self,
                    self.assets
                )

        self.content_frame.track_element(entry_form)
        self.content_frame.refresh_elements()
        self.content_frame.scroll_frame(1)
        entry_form.focus()
        return entry_form

    def get_content_data(self):
        return [x.getData() for x in self.content_frame.get_tracking_list()]

    def get_error_list(self):
        error_status = [x.getError() for x in self.content_frame.get_tracking_list()]
        error_messages = []

        for index, error_ret in enumerate(error_status):
            if error_ret[0] is True:
                error_messages.append((index + 1, error_ret[1]))
        return error_messages
    
    def refresh_assets(self):
        for content in self.content_frame.get_tracking_list():
            if isinstance(content, AssetPreview):
                content.refreshPreview()

    def show_asset_window(self):
        asset_window = AssetWindow(self, 800, 700, self.assets)
        self.winfo_toplevel().wait_window(asset_window)

        # refresh all asset window
        self.refresh_assets()