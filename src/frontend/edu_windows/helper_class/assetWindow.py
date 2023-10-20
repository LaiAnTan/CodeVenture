import customtkinter as ctk
from .imageEntry import ImageEntryForm
from .codeEntry import CodeEntryForm

class AssetWindow(ctk.CTkToplevel):
    def __init__(self, master, height, width, assets) -> None:
        super().__init__(master)
        self.master = master

        self.assets = assets
        self.content_frames = []

        self.height = height
        self.width = width

        self.entry_widget_heigth = height * 0.35
        self.entry_widget_width = (width - 45)

        self.wait_visibility()
        self.focus_set()
        self.grab_set()

        self.resizable(False, False)
        self.geometry(f"{width}x{height}")
        self.title("Available Assets")

        self.header = ctk.CTkFrame(self, width=width, height=55)
        self.header.grid(row=0, column=0, sticky='ew')

        self.content_frame = ctk.CTkFrame(self, width=width, height=height - 55)
        self.content_frame.grid(row=1, column=0)

        self.protocol("WM_DELETE_WINDOW", self.save_data)

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
        save_and_quit.pack(side=ctk.LEFT, padx=(10, 5), pady=5)

        add_new = ctk.CTkButton(
            self.header,
            text="Add New Asset",
            command=self.add_new_asset
        )
        add_new.pack(side=ctk.RIGHT, padx=5, pady=5)

        self.chosen_type = ctk.StringVar(value='Picture')
        asset_type = ['Picture', 'Code Snippet']
        type = ctk.CTkOptionMenu(
            self.header,
            values=asset_type,
            variable=self.chosen_type
        )
        type.pack(side=ctk.RIGHT, padx=(5, 10), pady=5)

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
        self.assets.clear()
        self.assets.extend([x.getData() for x in self.content_frames])

        # print(self.assets)

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
