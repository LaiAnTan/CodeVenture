import customtkinter as ctk
from .EntryForm import EntryForm
from PIL import Image, UnidentifiedImageError
from config import ASSET_DIR
from os import path

class ImageEntryForm(EntryForm):
    def __init__(self, master, parent, height, width, data=None):
        super().__init__(master, parent, height, width)

        self.type = "image"
        self.subwidth = self.width - 20
        self.subheight = self.height - 10
        self.max_image_height = self.subheight + 60
        self.previous_data = data
        self.SetFrames(True)

    def SetContentFrame(self):
        DirectoryAndNameFrame = ctk.CTkFrame(self.content, width=self.subwidth)
        DirectoryAndNameFrame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ImageNameLabel = ctk.CTkLabel(
            DirectoryAndNameFrame,
            text="Image's Name"
        )
        ImageNameLabel.grid(row=0, column=0, padx=5, pady=5)

        self.NameVar = ctk.StringVar(value='')
        self.NameEntry = ctk.CTkEntry(
            DirectoryAndNameFrame,
            width=self.subwidth * 0.2,
            textvariable=self.NameVar
        )
        self.NameEntry.grid(row=0, column=1, padx=5, pady=5)

        ContentEntryFormLabel = ctk.CTkLabel(
            DirectoryAndNameFrame,
            text="Image's Directory"
        )
        ContentEntryFormLabel.grid(row=0, column=2, padx=5, pady=5)

        self.DirectoryVar = ctk.StringVar(value='')
        self.ContentEntryForm = ctk.CTkEntry(
            DirectoryAndNameFrame,
            width=self.subwidth * 0.4,
            textvariable=self.DirectoryVar
        )
        self.ContentEntryForm.grid(row=0, column=3, padx=5, pady=5)
        self.DirectoryEntry = self.ContentEntryForm
        self.DirectoryEntry.bind("<Return>", lambda x : self.PreviewImage(self.DirectoryEntry.get().strip()))

        FileDialogImage = Image.open(f'{ASSET_DIR}/file_explorer.png')
        FileDialogButton = ctk.CTkButton(
            DirectoryAndNameFrame,
            text='',
            width=30,
            image=ctk.CTkImage(FileDialogImage, size=(20,20)),
            command=self.PromptFileDialog
        )
        FileDialogButton.grid(row=0, column=4, padx=5, pady=5)

        PreviewFrame = ctk.CTkFrame(self.content, width=self.subwidth, height=self.subheight)
        PreviewFrame.grid(row=1, column=0, padx=5, pady=5)

        self.PreviewLabel = ctk.CTkLabel(
            PreviewFrame, 
            text='No file selected',
            width=self.subwidth,
            height=self.subheight
        )
        self.PreviewLabel.grid(row=0, column=0, padx=5, pady=5)

        if self.previous_data is not None:
            self.DirectoryVar.set(self.previous_data[2])
            self.NameVar.set(self.previous_data[1])
            self.PreviewImage(self.previous_data[2])

    def getData(self):
        """returns data input into the frame in the following format 
        
        (type, image name, image directory)"""
        return (
            self.type,
            self.NameVar.get(),
            self.DirectoryVar.get()
        )

    ## helper functions

    def ratio_resizing(self, image: Image, max_height, max_width):
        """Resizes an image so that its height and width are within the set range"""
        width, height = image.size

        if width < max_width and height < max_height:
            return width, height

        x_percent = width / max_width 
        y_percent = height / max_height 
        percent = max(x_percent, y_percent)

        return int(width / percent), int(height / percent)

    def PromptFileDialog(self):
        """Prompts a file dialog for user to choose the file, then displayes the image"""
        file_path = ctk.filedialog.askopenfilename()
        self.PreviewImage(file_path)

    def PreviewImage(self, file_path):
        if not file_path:
            return
        directory = file_path
        file_format = file_path.split('.')[-1]

        if file_format not in ['jpeg', 'png', 'jpg']:
            print('LOG: Invalid File Format for Images')
            txt_c = 'red'
            name = 'Invalid File Format'
            previewimage = Image.open(f'{ASSET_DIR}/cant_display_image.png')
            size = (65, 65)
        else:
            txt_c = 'black'
            name = path.split(file_path)[-1].split('.')[0]

            try:
                previewimage = Image.open(directory)
                size=self.ratio_resizing(previewimage, self.max_image_height, self.subwidth)
            except (FileNotFoundError, UnidentifiedImageError):
                previewimage = Image.open(f'{ASSET_DIR}/cant_display_image.png')
                size = (65, 65)

        self.PreviewLabel.configure(
            text='',
            image=ctk.CTkImage(
                previewimage,
                size=size
            )
        )

        self.DirectoryEntry.configure(text_color=txt_c)
        self.DirectoryVar.set(directory)

        self.NameEntry.configure(text_color=txt_c)
        self.NameVar.set(name)

        return "break"