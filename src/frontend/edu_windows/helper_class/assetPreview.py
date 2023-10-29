import customtkinter as ctk
from .assetWindow import AssetWindow
from .entryForm import EntryForm
from ...std_windows.helper_class.imagelabel import ImageLabel
from .codeFromBuffer import CodeBufferRunner


class AssetSelectionScreen(AssetWindow):
    class DescriptionMessage(ctk.CTkFrame):
        def __init__(self, master, parent, width, height, name: str, data: tuple[str]):
            super().__init__(master, width=width, height=height)

            self.parent = parent
            self.name: str = name
            self.data: tuple[str] = data

            nameLabel = ctk.CTkLabel(
                self,
                text='Attachment Name: '
            )
            nameLabel.pack(side=ctk.LEFT, padx=5, pady=5)

            nameEntry_Var = ctk.StringVar(value=self.data[1])
            nameEntry = ctk.CTkEntry(
                self,
                width=140,
                state=ctk.DISABLED,
                textvariable=nameEntry_Var
            )
            nameEntry.pack(side=ctk.LEFT, padx=5, pady=5)

            button = ctk.CTkButton(
                self,
                text='Select',
                command=self.selection
            )
            button.pack(side=ctk.RIGHT, padx=5, pady=5)
        
        def selection(self):
            self.parent.selected_asset = self.data
            self.parent.destroy()

    def __init__(self, master, height, width, asset) -> None:
        super().__init__(master, height, width, asset)
        self.resizable(False, False)
        self.geometry(f"{width}x{height}")
        self.title("Select Asset")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.selected_asset = None

    def set_Header(self):
        guide = ctk.CTkLabel(
            self.header,
            text="Select the asset to attach to the file"
        )
        guide.rowconfigure(0, weight=1)
        guide.columnconfigure(0, weight=1)
        guide.grid(row=0, column=0, padx=10, pady=10)

    def set_Content(self):
        self.description_frames = ctk.CTkScrollableFrame(
            self.content,
            width=self.width - 45,
            height=self.height - 85
        )
        self.description_frames.columnconfigure(0, weight=1)
        self.description_frames.grid(row=0, column=0, padx=10, pady=10)

        for index, asset in enumerate(self.assets):
            self.description_frames.rowconfigure(index, weight=1)
            data_repr = AssetSelectionScreen.DescriptionMessage(
                self.description_frames,
                self,
                self.entry_widget_width,
                35,
                asset[1],
                asset
            )
            data_repr.grid(row=index, column=0, padx=10, pady=10, sticky='new')

    def get_Selection(self):
        return self.selected_asset

class AssetPreview(EntryForm):
    def __init__(self, master, parent, asset_list) -> None:
        super().__init__(master, parent)

        self.type = 'asset'

        self.assets : list[tuple[str]] = asset_list
        self.displaying_value = None
        self.SetFrames()

    def SetContentFrame(self):
        self.content.rowconfigure((0, 1), weight=1)
        self.content.columnconfigure(0, weight=1)

        self.display_default()
        self.ContentEntryForm = self.button


    def display_default(self):
        for children in self.content.winfo_children():
            children.grid_forget()

        header = ctk.CTkFrame(self.content)
        header.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        header.rowconfigure(0, weight=1)
        header.columnconfigure((0, 1), weight=1)

        label = ctk.CTkLabel(
            header,
            text="Select an asset to attach",
        )
        label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.button = ctk.CTkButton(
            header,
            text='Select an asset',
            command=self.display_Selection
        )
        self.set_focus_widget(self.button)
        self.button.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    

    def display_Selection(self):
        selection = AssetSelectionScreen(self, 450, 700, self.assets)
        self.winfo_toplevel().wait_window(selection)

        self.displaying_value = selection.get_Selection()
        if self.displaying_value is None:
            return 

        self.error = False
        self.refreshPreview()

    def set_displaying_value(self, display_val):
        self.displaying_value = display_val

    def refreshPreview(self):
        if self.displaying_value is None:
            return self.display_default()

        try:
            self.assets.index(self.displaying_value)
        except ValueError:
            return self.displayError()

        for children in self.content.winfo_children():
            children.grid_forget()

        header_frame = ctk.CTkFrame(self.content)
        header_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        asset_name_label = ctk.CTkLabel(
            header_frame,
            text=f'Name:'
        )
        asset_name_label.pack(side=ctk.LEFT, padx=(10, 5), pady=5)

        asset_name_var = ctk.StringVar(value=self.displaying_value[1])
        asset_name = ctk.CTkEntry(
            header_frame,
            width=140,
            textvariable=asset_name_var,
            state=ctk.DISABLED,
        )
        asset_name.pack(side=ctk.LEFT, padx=5, pady=5)

        asset_type = ctk.CTkLabel(
            header_frame,
            text=f'Type: {self.displaying_value[0].capitalize()}'
        )
        asset_type.pack(side=ctk.LEFT, padx=5, pady=5)

        self.button = ctk.CTkButton(
            header_frame,
            text='Change Attachment',
            command=self.display_Selection
        )
        self.button.pack(side=ctk.RIGHT, padx=5, pady=5)

        previewframe = ctk.CTkFrame(self.content)
        previewframe.columnconfigure(0, weight=1)
        previewframe.rowconfigure(0, weight=1)
        previewframe.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        match self.displaying_value[0]:
            case 'code':
                preview_label = CodeBufferRunner(
                    previewframe,
                    450,
                    self.displaying_value[1],
                    self.displaying_value[2],
                    self.displaying_value[3]
                )
            case 'image':
                preview_label = ImageLabel(
                    previewframe,
                    self.displaying_value[2],
                    450,
                    250,
                )
        preview_label.grid(row=0, column=0, padx=5, pady=5)

    def displayError(self):
        self.error = True
        self.error_msg = 'Invalid Asset Selected'

        for children in self.content.winfo_children():
            children.grid_forget()

        header = ctk.CTkFrame(self.content)
        header.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        header.rowconfigure(0, weight=1)
        header.columnconfigure((0, 1), weight=1)

        label = ctk.CTkLabel(
            header,
            text="ERROR: Asset is removed from asset set, please choose another one!",
            text_color='red'
        )
        label.pack(side=ctk.LEFT, padx=5, pady=5)

        self.button = ctk.CTkButton(
            header,
            text='Select another asset',
            command=self.display_Selection
        )
        self.button.pack(side=ctk.RIGHT, padx=5, pady=5)

    def getData(self):
        return (
            'asset',
            self.displaying_value
        )

    def importData(self, data: tuple[str]):
        if data[0] != 'asset':
            raise AssertionError('Wrong Type')
        
        super().importData(data)
        self.displaying_value = data[1]
        self.refreshPreview()