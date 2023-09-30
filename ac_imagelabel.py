import customtkinter as ctk

from PIL import Image
from PIL.ImageOps import invert

class ImageLabel(ctk.CTkFrame):
    def	__init__(self, master, img_path, max_img_width, has_invert: bool=False) -> None:
        super().__init__(master)

        self.img_path = img_path
        self.img = Image.open(img_path)
        self.max_width = max_img_width
        self.size = self.ImageResizer()
        self.invert = has_invert

        self.SetUpFrame()

    def ImageResizer(self):
        width, height = self.img.size
        if width > self.max_width:
            height = (height * self.max_width) / width
            width = self.max_width
        return width, height

    def SetUpFrame(self, has_invert: bool=False) -> None:
        ctk.CTkLabel(
            self,
            image = ctk.CTkImage(
                light_image=self.img,
                dark_image=invert(self.img) if self.invert else self.img,
                size=self.size
            ),
            text=""
        ).grid(row=0, column=0)
