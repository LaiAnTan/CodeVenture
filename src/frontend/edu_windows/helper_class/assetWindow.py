import customtkinter as ctk
from .imageEntry import ImageEntryForm
from .codeEntry import CodeEntryForm
from .errorWindow import ErrorWindow
from .refreshScrollFrame import RefreshableScrollableFrame

class AssetWindow(ctk.CTkToplevel):
    """
    Asset window used to add, remove and display asset used
    in an activity
    """
    def __init__(self, master, height, width, assets) -> None:
        super().__init__(master)
        self.master = master

        self.assets = assets

        self.height = height
        self.width = width

        self.entry_widget_heigth = height * 0.35
        self.entry_widget_width = (width - 45)

        self.wait_visibility()
        self.focus_set()
        self.grab_set()

        self.types = ['Picture', 'Code Snippet']

        self.geometry(f"{width}x{height}")
        self.title("Available Assets")

        self.header = ctk.CTkFrame(self)
        self.header.grid(row=0, column=0, sticky='ew')

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=1, column=0, sticky='ew')

        self.set_Frames()

    def set_Frames(self):
        """
        Sets frames in the window
        """
        self.set_Header()
        self.set_Content()

    def set_Header(self):
        """
        initializes the header frame of the window
        """
        save_and_quit = ctk.CTkButton(
            self.header,
            text="Save and Exit",
            command=self.save_data
        )
        save_and_quit.pack(side=ctk.RIGHT, padx=5, pady=5)

        self.chosen_type = ctk.StringVar(value='Picture')
        type = ctk.CTkOptionMenu(
            self.header,
            values=self.types,
            variable=self.chosen_type
        )
        type.pack(side=ctk.LEFT, padx=(5, 20), pady=5)

        add_new = ctk.CTkButton(
            self.header,
            text="Add New Asset",
            command=self.add_new_asset
        )
        add_new.pack(side=ctk.LEFT, padx=5, pady=5)

    def set_Content(self):
        """
        initializes the content frame of the window
        """
        self.asset_frame = RefreshableScrollableFrame(
            self.content,
            width=self.width - 25,
            height=self.height - 55
        )
        self.asset_frame.grid(row=0, column=0)

        if self.assets:
            for asset in self.assets:
                self.add_existing_asset(asset)
            self.asset_frame.refresh_elements()

    def add_existing_asset(self, data):
        """
        adds an asset with the information provided in data

        information provided in data may be a 
        Image
        """
        match data[0]:
            case 'image':
                entry_form = ImageEntryForm(
                    self.asset_frame,
                    self,
                )
            case 'code':
                entry_form = CodeEntryForm(
                    self.asset_frame,
                    self,
                )
        entry_form.importData(data)
        self.asset_frame.track_element(entry_form)

    def get_error_message(self) -> list[tuple[str]]:
        """
        Gets error that may occured in the window

        Formats the error message in the following way
        (where it happend, [list of errors])
        """
        error_status = [x.getError() for x in self.asset_frame.get_tracking_list()]
        error_messages = []

        for index, error_ret in enumerate(error_status):
            if error_ret:
                error_messages.append((index + 1, error_ret))

        return error_messages

    def save_data(self) -> None:
        """
        Saves asset in editor with the new asset list stored in window

        if error occured in the window, displays the list of errors in a seperate window
        then returns back to asset window
        """
        error_messages = self.get_error_message()
        if error_messages:
            error_window = ErrorWindow(self, 450, 550, error_messages, 'save assets')
            self.winfo_toplevel().wait_window(error_window)
            return

        self.assets.clear()
        self.assets.extend([x.getData() for x in self.asset_frame.get_tracking_list()])
        self.destroy()

    def add_new_asset(self) -> ImageEntryForm | CodeEntryForm:
        """
        Adds a new asset

        Asset can either be Picture or a Code Snippet

        Type is determined by chosen_type String Variable, which changes
        based on Option Menu
        """
        to_add  = self.chosen_type.get()
        match to_add:
            case 'Picture':
                entry_form = ImageEntryForm(
                    self.asset_frame,
                    self,
                )
            case 'Code Snippet':
                entry_form = CodeEntryForm(
                    self.asset_frame,
                    self,
                )
        self.asset_frame.track_element(entry_form)
        self.asset_frame.refresh_elements()
        self.asset_frame.scroll_frame(1)
        entry_form.focus()

        return entry_form
