import customtkinter as ctk

from .paragraphEntry import ParagraphEntryForm
from .assetPreview import AssetPreview
from .assetWindow import AssetWindow
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
        asset_adder_frame.columnconfigure((0, 1), weight=1)
        asset_adder_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        asset_button = ctk.CTkButton(
            asset_adder_frame,
            image=asset_folder_image,
            text='Assets',
            width=0,
            command=self.show_asset_window
        )
        asset_button.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        option_frame = ctk.CTkFrame(asset_adder_frame, fg_color='transparent')
        option_frame.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        option_label = ctk.CTkLabel(
            option_frame,
            text='Type: ',
        )
        option_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.chosen_para_type = ctk.StringVar(value='Paragraph')
        self.para_types = ['Paragraph', 'Asset']
        add_options = ctk.CTkOptionMenu(
            option_frame,
            values=self.para_types,
            variable=self.chosen_para_type
        )
        add_options.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        add_button = ctk.CTkButton(
            option_frame,
            text="Add Entry Form At the End!",
            width=0,
            command=lambda : self.add_entry_point()
        )
        add_button.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        self.content_frame = RefreshableScrollableFrame(
            self,
        )
        self.content_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nswe')

    def add_entry_point(self) -> ParagraphEntryForm | AssetWindow:
        """Adds an certain type of entry form at the end of the window
        
        type is retrive from add_options CtkOptionMenu"""
        to_add = self.chosen_para_type.get()

        entry_form = self.widget_factory(to_add)

        self.content_frame.track_element(entry_form)
        self.content_frame.refresh_elements()
        self.content_frame.scroll_frame(1)
        entry_form.focus()
        return entry_form

    def widget_factory(self, to_add) -> ParagraphEntryForm | AssetWindow:
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

    def import_data_list(self, data_list = list[tuple[str]]):
        for data in data_list:
            entry_form = self.widget_factory(data[0].capitalize())
            entry_form.importData(data)

            self.content_frame.track_element(entry_form)
            entry_form.focus()
        self.content_frame.refresh_elements()