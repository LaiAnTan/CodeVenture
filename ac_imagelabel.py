import customtkinter as ctk

from PIL import Image
from PIL.ImageOps import invert

class ImageLabelGen():
    def	__init__(self, img_path, max_img_width, attach_frame) -> None:
        self.img_path = img_path
        self.img = Image.open(img_path)
        self.max_width = max_img_width
        self.size = self.ImageResizer()
        self.frame = attach_frame

    def ImageResizer(self):
        width, height = self.img.size
        if width > self.max_width:
            height = (height * self.max_width) / width
            width = self.max_width
        return width, height

    def ImageLabelGen(self, has_invert: bool=False) -> None:
        ret_widget = ctk.CTkLabel(
            self.frame,
            image= ctk.CTkImage(
                light_image=self.img,
                dark_image=invert(self.img) if has_invert else self.img,
                size=self.size
            ),
            text=""
        )
        return ret_widget
