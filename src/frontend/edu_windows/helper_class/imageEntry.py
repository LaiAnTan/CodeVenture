import customtkinter as ctk
from .entryForm import EntryForm
from PIL import Image, UnidentifiedImageError
from config import ASSET_DIR
from os import path

class ImageEntryForm(EntryForm):
    def __init__(self, master, parent):
        super().__init__(master, parent)

        self.type = "image"
        self.max_image_height = 250
        self.max_image_width = 550
        self.error_msg = ''
        self.SetFrames(True)

    def SetContentFrame(self):
        DirectoryAndNameFrame = ctk.CTkFrame(self.content)
        DirectoryAndNameFrame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ImageNameLabel = ctk.CTkLabel(
            DirectoryAndNameFrame,
            text="Image's Name"
        )
        ImageNameLabel.grid(row=0, column=0, padx=5, pady=5)

        self.NameVar = ctk.StringVar(value='')
        self.NameEntry = ctk.CTkEntry(
            DirectoryAndNameFrame,
            textvariable=self.NameVar
        )
        self.NameEntry.grid(row=0, column=1, padx=5, pady=5)

        ContentEntryFormLabel = ctk.CTkLabel(
            DirectoryAndNameFrame,
            text="Image's Directory"
        )
        ContentEntryFormLabel.grid(row=0, column=2, padx=5, pady=5)

        self.DirectoryVar = ctk.StringVar(value='')
        self.DirectoryEntry = ctk.CTkEntry(
            DirectoryAndNameFrame,
            textvariable=self.DirectoryVar
        )
        self.set_focus_widget(self.DirectoryEntry)
        self.DirectoryEntry.grid(row=0, column=3, padx=5, pady=5)
        self.DirectoryEntry.bind("<Return>", lambda x : self.PreviewImage(self.DirectoryEntry.get().strip()))

        FileDialogImage = Image.open(f'{ASSET_DIR}/file_explorer.png')
        FileDialogButton = ctk.CTkButton(
            DirectoryAndNameFrame,
            text='',
            image=ctk.CTkImage(FileDialogImage, size=(20,20)),
            command=self.PromptFileDialog
        )
        FileDialogButton.grid(row=0, column=4, padx=5, pady=5)

        PreviewFrame = ctk.CTkFrame(self.content)
        PreviewFrame.columnconfigure(0, weight=1)
        PreviewFrame.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.PreviewLabel = ctk.CTkLabel(
            PreviewFrame, 
            text='No file selected',
        )
        self.PreviewLabel.grid(row=0, column=0, padx=5, pady=5)

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

    def ErrorImage(self, error_msg, original_dir):
        self.error_msg = error_msg

        self.PreviewLabel.configure(
            text='',
            image=ctk.CTkImage(
                Image.open(f'{ASSET_DIR}/cant_display_image.png'),
                size=(65, 65)
            )
        )

        self.DirectoryEntry.configure(text_color='red')
        self.DirectoryVar.set(original_dir)

        self.NameEntry.configure(text_color='red')
        self.NameVar.set('Invalid File Format')

        return "break"

    def PreviewImage(self, file_path):
        if not file_path:
            return
        directory = file_path
        file_format = file_path.split('.')[-1]

        if file_format not in ['jpeg', 'png', 'jpg']:
            # print('LOG: Invalid File Format for Images')
            return self.ErrorImage('Error in Image Attachment - Invalid File Format', directory)
        else:
            txt_c = 'white'
            name = path.split(file_path)[-1].split('.')[0]
            try:
                previewimage = Image.open(directory)
                size=self.ratio_resizing(previewimage, self.max_image_height, self.max_image_width)
            except (FileNotFoundError, UnidentifiedImageError):
                return self.ErrorImage('Error in Image Asset - Unable to Open File', directory)

        self.PreviewLabel.configure(
            text='',
            image=ctk.CTkImage(
                previewimage,
                size=size
            )
        )

        self.DirectoryEntry.configure(text_color=txt_c)
        self.DirectoryVar.set(directory)
        self.NameVar.set(name)
        self.NameEntry.configure(text_color=txt_c)

        return "break"

    def importData(self, data: tuple[str]):
        if data[0] != 'image':
            raise AssertionError("Wrong Type")

        super().importData(data)
        self.PreviewImage(data[2])
        self.NameVar.set(data[1])

    def getError(self):
        error_list = []

        if self.DirectoryEntry.get() == '' and self.NameEntry.get() == '':
            error_list.append('Image entry not used, remove if not needed')
        else:
            if self.DirectoryEntry.get() == '':
                error_list.append('No image provided')
            if self.NameEntry.get() == '':
                error_list.append('No name provided')
            if self.DirectoryEntry.cget('text_color') == 'red':
                error_list.append(self.error_msg)

        return error_list