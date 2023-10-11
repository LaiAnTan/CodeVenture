import pygments as pyg
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

import os
import sys

import customtkinter as ctk

import subprocess

from .imagelabel import ImageLabel

class CodeRunner(ctk.CTkFrame):
    def __init__(self, master, max_img_width, code_name, activity_folder) -> None:
        self.max_width = max_img_width

        self.code_name = code_name
        self.activity_folder = activity_folder

        self.code_folder = f"{self.activity_folder}/{self.code_name}"

        if master != None:
            super().__init__(master)

            self.HeaderFrame = ctk.CTkFrame(self)
            self.HeaderFrame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            self.CodeFrame = ctk.CTkFrame(self)
            self.CodeFrame.grid(row=1, column=0, padx=5, pady=5,)

            self.RunButtonFrame = ctk.CTkFrame(self)
            self.RunButtonFrame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
            self.RunButtonFrame.columnconfigure(0, weight=1)

            self.outputFrame = ctk.CTkFrame(self)

            self.setUpFrame()

    def	DisplayCodeline_FromFile(self):
        with open(f"{self.code_folder}/main.py") as file:
            pyg.highlight(
                file.read(),
                PythonLexer(),
                ImageFormatter(
                    font_name="Noto Sans Mono",
                    font_size=12
                ),
                outfile=f"{self.code_folder}/temp"
            )

        ret_widget = ImageLabel(
            self.CodeFrame,
            f"{self.code_folder}/temp",
            self.max_width,
            True
        )

        ## imagine if this is system24, LETS GO
        os.remove(f"{self.code_folder}/temp")

        return ret_widget

    def	setUpFrame(self):
        title = ctk.CTkLabel(
            self.HeaderFrame,
            text=self.code_name
        )
        title.grid(row=0, column=0, padx=5)

        RunButton = ctk.CTkButton(
            self.RunButtonFrame,
            text="Run",
            command=self.RunCode,
            height=10
        )
        RunButton.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        CodeContent = self.DisplayCodeline_FromFile()
        CodeContent.grid(row=0, column=0, padx=5, pady=5)

    def RunTestCases(self, testcase_path):
        cmd = f"{sys.executable} \"{self.code_folder}/main.py\""
        testcase_in = open(testcase_path)
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

        cmd = f"{sys.executable} \"{self.code_folder}/main.py\""
        code_input = open(f"{self.code_folder}/input")
        
        font_color = "white"
        try:
            code_output = subprocess.check_output(cmd, timeout=10, stdin=code_input, stderr=subprocess.STDOUT, shell=True).decode()
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
        placeholder.grid(row=0, column=0, padx=5, pady=5)

        self.outputFrame.grid(row=3, column=0, padx=5, pady=5)
