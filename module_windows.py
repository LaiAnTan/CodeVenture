import pygments as pyg
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

import customtkinter as ctk

from PIL import Image
from PIL.ImageOps import invert

from app import App
from module import Module
from window_gen import selection_screen

from code_runner import CodeRunner

from imagelabel import ImageLabelGen

class ModuleWindow():
    def	__init__(self, module: Module):
        self.module = module
    
    def ImageHandler(self, content, max_img_width, attach_frame):
        if self.module.img.get(content):
            ret_widget = ImageLabelGen(
                self.module.ModulePath + self.module.img[content],
                max_img_width - 50,
                attach_frame
            ).ImageLabelGen()
        else:
            ret_widget = ctk.CTkLabel(
                attach_frame,
                text=f"Error displaying image {content}",
                width=max_img_width,
                wraplength=max_img_width - 10,
            )
        return ret_widget
    
    def CodeHandler(self, content, max_img_width, attach_frame):
        if self.module.code.get(content):
            ret_widget = CodeRunner(max_img_width - 30,
                            attach_frame,
                            self.module.code[content],
                            self.module.ModulePath
                            ).setUpFrame()
        else:
            ret_widget = ctk.CTkLabel(
                attach_frame,
                text=f"Error displaying code {content}",
                width=max_img_width,
                wraplength=max_img_width - 10,
            )
        return ret_widget

    def FillFrames(self, attach: App):

        ## header details -------------------------------------------

        header_frame = ctk.CTkFrame(attach.main_frame)

        quiz_name = ctk.CTkLabel(
            header_frame,
            text=f"{self.module.id} {self.module.title}"
        )

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda : selection_screen(attach),
            width=20
        )

        quiz_name.pack(side=ctk.LEFT, padx=5, pady=5)
        back_button.pack(side=ctk.RIGHT, padx=5, pady=5)

        header_frame.grid(row=0, column=0, sticky="we", padx=5, pady=5)

        ## header details end --------------------------------------------

        content_frame = ctk.CTkFrame(attach.main_frame)

        ## main_content frame ----------------------------

        main_content_frame_width = 550

        main_content_frame = ctk.CTkScrollableFrame(
            content_frame,
            width=main_content_frame_width,
            height=460
        )

        paragraph_frame_width = main_content_frame_width - 20

        for index, content in enumerate(self.module.content):
            paragraph_frame = ctk.CTkFrame(
                main_content_frame
            )

            match content[0]:
                case Module.Content_Type.Paragraph:
                    paragraph = ctk.CTkLabel(
                        paragraph_frame,
                        text=content[1],
                        width=paragraph_frame_width,
                        wraplength=paragraph_frame_width - 10,
                        anchor="w",
                        justify="left"
                    )

                case Module.Content_Type.Image:
                    paragraph = self.ImageHandler(
                        content[1],
                        paragraph_frame_width,
                        paragraph_frame
                    )

                case Module.Content_Type.Code:
                    paragraph = self.CodeHandler(
                        content[1],
                        paragraph_frame_width,
                        paragraph_frame
                    )

            paragraph.grid(row=0, column=0, padx=5, pady=5)
            paragraph_frame.grid(row=index, column=0, padx=5, pady=10)

        main_content_frame.grid(row=0, column=0, padx=5, pady=5)

        ## qna frame end -------------------------------

        ## some optional side bar start -----------------------

        sidebar_width = 50
        sidebar_frame = ctk.CTkFrame(
            content_frame,
            width=sidebar_width
        )

        some_label = ctk.CTkLabel(
            sidebar_frame,
            text="does module need a side bar tho....?",
            width=sidebar_width,
            wraplength=sidebar_width,
        )

        some_label.grid(row=0, column=0, padx=5, pady=5)

        sidebar_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

        ## some optional side bar end ----------------------------

        content_frame.grid(row=1, column=0, padx=5, pady=5,)

        ## footer ---------------------------------------------

        footer_frame = ctk.CTkFrame(
            attach.main_frame,
        )

        submit_button = ctk.CTkButton(
            footer_frame,
            text="Complete",
            width=150,
            command= self.__beep_boop_button
        )

        submit_button.grid(row=0, column=0, padx=0, pady=0)

        footer_frame.grid(row=2, column=0, padx=5, pady=5)

        ## footer end ------------------------------------------

    def __beep_boop_button(self):
        print("yeah yeah yeah setting it to completed...")
        return True