from ..ui_app import App
from .edu_activity_editor import ActivityEditor
from .helper_class.errorWindow import ErrorWindow
from .helper_class.dataFileEditor import dataFileEditor
from ...backend.factory.ModuleFactory import ModuleFactory
from ...backend.activity.ac_classes.ac_module import Activity, Module


class ModuleEditor(ActivityEditor):

    """
    Frame class for displaying the module editor window for educators.
    """

    def __init__(self, existing_module: Module = None):
        """
        Initialises the class.
        """

        super().__init__(Activity.AType['Module'], existing_module)

        self.SetFrames()
        if self.editing:
            self.import_data()

    def import_data(self):
        ac_data = []

        for content in self.ac.content:
            type = content[0]
            value = content[1]
            match type:
                case Activity.Content_Type.Paragraph:
                    widget_type = 'paragraph'
                    widget_content = value
                case Activity.Content_Type.Code | Activity.Content_Type.Image:
                    widget_type = 'asset'
                    widget_content = self.ref_asset_dic[value]
            ac_data.append((widget_type, widget_content))

        self.data_editor.import_data_list(ac_data)

    def ContentData(self):
        """
        Add content data into frame.
        """

        self.content_data.rowconfigure(0, weight=1)
        self.content_data.columnconfigure(0, weight=1)

        self.data_editor = dataFileEditor(
            self.content_data,
            self.asset
        )
        self.data_editor.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    # helper functions

    def GetContentData(self):
        """
        Getter for content data.
        """
        return self.data_editor.get_content_data()

    def get_error_list(self):
        """
        Getter for error list.
        """

        return self.data_editor.get_error_list()

    def ExportData(self):
        """
        Handles the event where the module is exported.
        """
        print('LOG: Exporting...')
        error_messages = []

        # check header
        header_error = self.get_header_errors()
        if header_error[1]:
            error_messages.append(header_error)

        # check content
        error_messages.extend(self.get_error_list())

        if error_messages:
            error_window = ErrorWindow(self, 450, 550, error_messages,
                                       'export Module')
            self.winfo_toplevel().wait_window(error_window)
            return False

        header = self.GetHeaderData()
        content = self.GetContentData()

        ModuleFactory(header, content, self.asset).build()
        print('Export Complete!')
        return True

    def get_asset_list(self):
        """
        Getter for asset list.
        """

        return self.asset


if __name__ == "__main__":
    App().change_frame(ModuleEditor(None))
    App().mainloop()
