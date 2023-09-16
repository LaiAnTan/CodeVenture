import pygments as pyg
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

from PIL import Image
from PIL.ImageOps import invert

import os
import sys

import customtkinter as ctk

import subprocess

from imagelabel import ImageLabelGen

class CodeRunner():
    def __init__(self, max_img_width, attach_frame, code_name, root_path) -> None:
        self.max_width = max_img_width
        self.attach_frame = attach_frame
        self.code_name = code_name
        self.root_path = root_path

        self.CodeRunnerFrame = ctk.CTkFrame(
            self.attach_frame
        )

        self.HeaderFrame = ctk.CTkFrame(
            self.CodeRunnerFrame
        )

        self.RunButtonFrame = ctk.CTkFrame(
            self.CodeRunnerFrame
        )

        self.RunButtonFrame.columnconfigure(
            0,
            weight=1
        )

        self.CodeFrame = ctk.CTkFrame(
            self.CodeRunnerFrame
        )

        self.outputFrame = ctk.CTkFrame(
            self.CodeRunnerFrame
        )

    def	DisplayCodeline_FromFile(self):
        code_content = []
        with open(self.root_path + self.code_name) as file:
            pyg.highlight(
                file.read(),
                PythonLexer(),
                ImageFormatter(
                    font_name="Noto Sans Mono",
                    font_size=12
                ),
                outfile=f"{self.root_path}temp"
            )

        ret_widget = ImageLabelGen(
            self.root_path + "temp",
            self.max_width,
            self.CodeFrame
        ).ImageLabelGen(True)

        ## imagine if this is system24, LETS GO
        os.remove(f"{self.root_path}temp")

        return ret_widget

    def	setUpFrame(self):
        title = ctk.CTkLabel(
            self.HeaderFrame,
            text=self.code_name
        )

        title.grid(
            row=0,
            column=0,
            padx=5
        )

        RunButton = ctk.CTkButton(
            self.RunButtonFrame,
            text="Run",
            command=self.RunCode,
            height=10
        )

        RunButton.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        CodeContent = self.DisplayCodeline_FromFile()

        CodeContent.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.HeaderFrame.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.CodeFrame.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
        )

        self.RunButtonFrame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        return self.CodeRunnerFrame

    def RunTestCases(self, testcases):
        cmd = f"{sys.executable} {self.root_path}{self.code_name}"
        testcase_in = open(f"{self.root_path}{testcases}")
        try:
            code_output = subprocess.check_output(cmd, timeout=10, stdin=testcase_in, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as errxc:
            code_output = errxc.output
        except subprocess.TimeoutExpired:
            code_output = "Timeout After Running For 10 seconds"

        return code_output

    def RunCode(self):
        for widget in self.outputFrame.winfo_children():
            widget.destroy()
        self.outputFrame.forget()

        print("Running Code. BzzZt")

        cmd = f"{sys.executable} {self.root_path}{self.code_name}"
        font_color = "white"
        try:
            code_output = subprocess.check_output(cmd, timeout=10, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as errxc:
            code_output = errxc.output
            font_color = "red"
        except subprocess.TimeoutExpired:
            code_output = "Timeout After Running For 10 seconds"
            font_color = "red"

        placeholder = ctk.CTkLabel(
            self.outputFrame,
            text=code_output,
            width=self.max_width - 50,
            wraplength=self.max_width - 70,
            anchor="w",
            justify="left",
            font=ctk.CTkFont("Noto Sans Mono", size=11),
            bg_color="black",
            text_color=font_color
        )

        placeholder.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.outputFrame.grid(
            row=3,
            column=0,
            padx=5,
            pady=5
        )
