import customtkinter as ctk
from .imageEntry import ImageEntryForm, EntryForm
from .codeEntry import CodeEntryForm
from .errorWindow import ErrorWindow

class AssetWindow(ctk.CTkToplevel):
    def __init__(self, master, height, width, assets) -> None:
        super().__init__(master)
        self.master = master

        self.assets = assets
        self.content_frames: list[EntryForm] = []

        self.height = height
        self.width = width

        self.entry_widget_heigth = height * 0.35
        self.entry_widget_width = (width - 45)

        self.wait_visibility()
        self.focus_set()
        self.grab_set()

        self.resizable(0, 0)
        self.geometry(f"{width}x{height}")
        self.title("Available Assets")

        self.header = ctk.CTkFrame(self)
        self.header.grid(row=0, column=0, sticky='ew')

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, sticky='ew')

        self.set_Frames()

    def set_Frames(self):
        self.set_Header()
        self.set_Content()

    def set_Header(self):
        save_and_quit = ctk.CTkButton(
            self.header,
            text="Save and Exit",
            command=self.save_data
        )
        save_and_quit.pack(side=ctk.RIGHT, padx=5, pady=5)

        self.chosen_type = ctk.StringVar(value='Picture')
        asset_type = ['Picture', 'Code Snippet']
        type = ctk.CTkOptionMenu(
            self.header,
            values=asset_type,
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
        self.asset_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            width=self.width - 25,
            height=self.height - 55
        )
        self.asset_frame.grid(row=0, column=0)
        self.content_entry_frame = self.asset_frame

        for asset in self.assets:
            self.add_existing_asset(asset)

    def add_existing_asset(self, data):
        match data[0]:
            case 'image':
                entry_form = ImageEntryForm(
                    self.asset_frame,
                    self,
                    self.entry_widget_heigth,
                    self.entry_widget_width,
                    data
                )
            case 'code':
                entry_form = CodeEntryForm(
                    self.asset_frame,
                    self,
                    self.entry_widget_heigth,
                    self.entry_widget_width,
                    data
                )
        self.content_frames.append(entry_form)
        entry_form.grid(
            row=len(self.content_frames),
            column=0,
            padx=5,
            pady=5
        )

    def save_data(self):
        error_status = [x.getError() for x in self.content_frames]
        error_messages = []

        for index, error_ret in enumerate(error_status):
            if error_ret[0] is True:
                error_messages.append((index + 1, error_ret[1]))
        if error_messages:
            error_window = ErrorWindow(self, 450, 550, error_messages, 'save assets')
            self.master.winfo_toplevel().wait_window(error_window)
            return

        self.assets.clear()
        self.assets.extend([x.getData() for x in self.content_frames])
        self.destroy()

    def add_new_asset(self):
        to_add  = self.chosen_type.get()
        match to_add:
            case 'Picture':
                entry_form = ImageEntryForm(
                    self.asset_frame,
                    self,
                    self.entry_widget_heigth,
                    self.entry_widget_width,
                )
            case 'Code Snippet':
                entry_form = CodeEntryForm(
                    self.asset_frame,
                    self,
                    self.entry_widget_heigth,
                    self.entry_widget_width,
                )
        self.content_frames.append(entry_form)
        entry_form.grid(
            row=len(self.content_frames),
            column=0,
            padx=5,
            pady=5
        )
        self.ScrollContentFrame(1)
        entry_form.focus()


    def ScrollContentFrame(self, how_much: float):
        """Processes all idle and pending task
        Scroll the frame until value stated in how_much is offscreen at the top"""

        self.content_entry_frame.update_idletasks()
        self.content_entry_frame._parent_canvas.yview_moveto(str(how_much))
