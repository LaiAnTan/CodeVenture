import pygments as pyg
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

import os
import sys

import customtkinter as ctk

import subprocess

from ...std_windows.helper_class.imagelabel import ImageLabel
from config import ROOT_DIR

class CodeBufferRunner(ctk.CTkFrame):
    """
    a specific frame used to display code from a buffer
    
    if input buffer is None, code is unrunnable and is view only
    """
    def __init__(self, master, max_img_width, code_name, code_buffer, input_buffer) -> None:
        super().__init__(master)

        self.max_width = max_img_width

        self.code_name = code_name
        self.code_buffer = code_buffer
        self.input_buffer = input_buffer

        self.temp_file = f"{ROOT_DIR}/temp"
        self.temp_file_input = f"{ROOT_DIR}/temp2"

        self.runnable = input_buffer is not None

        self.HeaderFrame = ctk.CTkFrame(self)
        self.HeaderFrame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.CodeFrame = ctk.CTkFrame(self)
        self.CodeFrame.grid(row=1, column=0, padx=5, pady=5)

        if self.runnable:
            self.RunButtonFrame = ctk.CTkFrame(self)
            self.RunButtonFrame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
            self.RunButtonFrame.columnconfigure(0, weight=1)

        self.outputFrame = ctk.CTkFrame(self)

        self.setUpFrame()

    def	DisplayCodeline_FromBuffer(self):
        """
        Loads code content from code buffer and displays it as
        a syntax highlighted picture
        """
        pyg.highlight(
            self.code_buffer,
            PythonLexer(),
            ImageFormatter(
                font_name="Helvetica",
                font_size=12
            ),
            outfile=self.temp_file
        )

        ret_widget = ImageLabel(
            self.CodeFrame,
            self.temp_file,
            1600,
            self.max_width,
            True
        )

        os.remove(self.temp_file)

        return ret_widget

    def	setUpFrame(self):
        """
        Sets up contents in the widget
        """
        title = ctk.CTkLabel(
            self.HeaderFrame,
            text=self.code_name
        )
        title.grid(row=0, column=0, padx=5)


        if self.runnable:
            RunButton = ctk.CTkButton(
                self.RunButtonFrame,
                text="Run",
                command=self.RunCode,
                height=10
            )
            RunButton.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        CodeContent = self.DisplayCodeline_FromBuffer()
        CodeContent.grid(row=0, column=0, padx=5, pady=5)

    def RunCode(self):
        """
        Function to run the code stored in code buffer

        first loads code and input from buffer into a temporary file
        then runs the code

        Then, displays the code output

        timeout is set to 5 seconds and will automatically terminate after the
        set period of time has passed
        """
        for widget in self.outputFrame.winfo_children():
            widget.destroy()
        self.outputFrame.forget()

        print("Running Code. BzzZt")

        # dump buffer code value into a temporary python file
        with open(self.temp_file, '+w') as file:
            file.write(self.code_buffer)

        # dump input data into another temporary python file
        with open(self.temp_file_input, '+w') as file_input:
            file_input.write(self.input_buffer)

        # run the temporary python file
        cmd = f"{sys.executable} {self.temp_file}"

        font_color = "white"
        try:
            code_output = subprocess.check_output(cmd,
                                                  timeout=5,
                                                  stdin=open(self.temp_file_input),
                                                  stderr=subprocess.STDOUT,
                                                  shell=True).decode()
        except subprocess.CalledProcessError as errxc:
            code_output = errxc.output
            font_color = "red"
        except subprocess.TimeoutExpired:
            code_output = "Timeout After Running For 5 seconds"
            font_color = "red"

        # remove the file
        os.remove(self.temp_file)
        os.remove(self.temp_file_input)

        placeholder = ctk.CTkLabel(
            self.outputFrame,
            text=code_output,
            width=self.max_width - 50,
            wraplength=self.max_width - 70,
            anchor="w",
            justify="left",
            font=ctk.CTkFont("Helvetica", size=11),
            bg_color="black",
            text_color=font_color
        )
        placeholder.grid(row=0, column=0, padx=5, pady=5)

        self.outputFrame.grid(row=3, column=0, padx=5, pady=5)
