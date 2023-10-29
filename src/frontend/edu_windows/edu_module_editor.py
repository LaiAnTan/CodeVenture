import customtkinter as ctk
import os
from PIL import Image
from config import ASSET_FOLDER

from ..ui_app import App
from .edu_activity_editor import ActivityEditor
from ...backend.activity.ac_classes.ac_module import Activity, Module

from .helper_class.paragraphEntry import ParagraphEntryForm
from .helper_class.assetPreview import AssetPreview
from .helper_class.errorWindow import ErrorWindow
from .helper_class.dataFileEditor import dataFileEditor

from ...backend.factory.ModuleFactory import ModuleFactory

class ModuleEditor(ActivityEditor):
    def __init__(self, existing_module: Module = None):
        super().__init__(Activity.AType['Module'], existing_module)

        self.assets = []
        self.SetFrames()

    def ContentData(self):
        self.content_data.rowconfigure(0, weight=1)
        self.content_data.columnconfigure(0, weight=1)

        self.data_editor = dataFileEditor(
            self.content_data,
            self.assets
        )
        self.data_editor.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    ## helper functions

    def GetContentData(self):
        return self.data_editor.get_content_data()

    def get_error_list(self):
        return self.data_editor.get_error_list()

    def ExportData(self):
        print('LOG: Exporting...')

        error_messages = self.get_error_list()
        if error_messages:
            error_window = ErrorWindow(self, 450, 550, error_messages, 'export Module')
            self.winfo_toplevel().wait_window(error_window)
            return False

        header = self.GetHeaderData()
        content = self.GetContentData()

        ModuleFactory(header, content, self.assets).build()
        print('Export Complete!')
        return True

    def get_asset_list(self):
        return self.assets

if __name__ == "__main__":
    App().change_frame(ModuleEditor(None))
    App().mainloop()