import customtkinter as ctk

from PIL import Image
from PIL.ImageOps import invert
from config import ASSET_DIR


class ImageLabel(ctk.CTkFrame):

    """
    Class that handles displaying images in tkinter.

    Made to add additional functionality to ctklabel with an image in it.
    """

    def __init__(self, master, img_path,
                 max_img_height, max_img_width,
                 has_invert: bool = False) -> None:
        """
        Initialises the class.
        """
        super().__init__(master)

        self.img_path = img_path
        try:
            self.img = Image.open(img_path)
        except Exception as e:
            print(f"LOG: Error Happened: {e}")
            self.img = Image.open(f'{ASSET_DIR}/cant_display_image.png')

        self.max_height = max_img_height
        self.max_width = max_img_width
        self.size = self.ratio_resizing()
        self.invert = has_invert

        self.SetUpFrame()

    def ratio_resizing(self):
        """
        Resizes an image so that its height and width are within the set range
        """
        width, height = self.img.size

        if width < self.max_width and height < self.max_height:
            return width, height

        x_percent = width / self.max_width
        y_percent = height / self.max_height
        percent = max(x_percent, y_percent)

        return int(width / percent), int(height / percent)

    def SetUpFrame(self) -> None:
        """
        Creates and attaches the image to the main frame (master).
        """
        ctk.CTkLabel(
            self,
            image=ctk.CTkImage(
                light_image=self.img,
                dark_image=invert(self.img) if self.invert else self.img,
                size=self.size
            ),
            text=""
        ).grid(row=0, column=0)
