import pygments as pyg
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

from PIL import Image
from PIL.ImageOps import invert

import os
import sys

import customtkinter as ctk

import subprocess
from threading import Timer

import pexpect

class IDE():
    def __init__(self, max_img_width, attach_frame, code_name, id, root_path) -> None:
        self.max_width = max_img_width
        self.attach_frame = attach_frame
        self.code_name = f"{code_name}-{id}"
        self.root_path = root_path
        self.max_output_size = 68750
        ## please change this to a reasonable timeout period
        self.timeout_period = 10

        self.CodeIDEFrame = ctk.CTkFrame(
            self.attach_frame
        )

        self.RunButtonFrame = ctk.CTkFrame(
            self.CodeIDEFrame
        )

        self.RunButtonFrame.columnconfigure(
            0,
            weight=1
        )

        self.IDEFrame = ctk.CTkFrame(
            self.CodeIDEFrame,
        )

        self.InputFrame = ctk.CTkFrame(
            self.CodeIDEFrame
        )

        self.outputFrame = ctk.CTkFrame(
            self.CodeIDEFrame
        )


    def setUpIDEWindow(self):
        font = ctk.CTkFont(
            "Noto Sans Mono",
            size=12,
        )

        self.IDETextBox = ctk.CTkTextbox(
            self.IDEFrame,
            width=320,
            height=250,
            font=font,
            tabs=font.measure("    "),
            wrap=ctk.WORD
        )

        self.IDETextBox.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        return self.IDETextBox


    def setupInputFrame(self):
        font = ctk.CTkFont(
            "Noto Sans Mono",
            size=12,
        )

        self.input_textbox = ctk.CTkTextbox(
            self.InputFrame,
            width=320,
            height=120,
            font=font,
            tabs=font.measure("    "),
            wrap=ctk.WORD
        )

        self.input_textbox.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )
        
        return self.input_textbox


    def	setUpFrame(self):
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

        self.setUpIDEWindow()

        self.setupInputFrame()

        self.IDEFrame.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
        )

        self.InputFrame.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.RunButtonFrame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        return self.CodeIDEFrame

    def getContents(self):
        return self.IDETextBox.get("0.0", "end")

    def RunTestCases(self, testcases):
        ## open file and dump all data inside
        text = self.IDETextBox.get("0.0", "end")
        testcase_in = open(f"{self.root_path}{testcases}")

        with open(f"{self.root_path}{self.code_name}", "w") as file:
            file.write(text)

        cmd = f"{sys.executable} {self.root_path}{self.code_name}"
        try:
            code_output = subprocess.check_output(cmd, timeout=10, stdin=testcase_in, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as errxc:
            code_output = errxc.output
        except subprocess.TimeoutExpired:
            code_output = "Timeout After Running For 10 seconds"


        ## remove the file
        os.remove(f"{self.root_path}{self.code_name}")

        ## Returns the output
        ## if error, return the raw error output
        return code_output

    def RunCode(self):
        for widget in self.outputFrame.winfo_children():
            widget.destroy()
        self.outputFrame.forget()

        terminal_width = (self.max_width - 50)

        print("Running Code. BzzZt")

        ## open file and dump all data inside
        text = self.IDETextBox.get("0.0", "end")
        with open(f"{self.root_path}{self.code_name}", "w") as file:
            file.write(text)

        cmd = f"{sys.executable} {self.root_path}{self.code_name}"
        code_output = ""
        error_output = ""

        user_input = self.input_textbox.get("0.0", "end")
        user_input = bytes(user_input, "utf-8")

        try:
            code_runner = subprocess.run(cmd, timeout=10, input=user_input, capture_output=True, shell=True)
            code_output = code_runner.stdout
            error_output = code_runner.stderr
        except subprocess.TimeoutExpired:
            code_output = bytes("", "utf-8")
            error_output = bytes("Timeout After Running For 10 seconds", "utf-8")

        ## remove the file
        os.remove(f"{self.root_path}{self.code_name}")
        code_output.decode()

        code_output_frame = ctk.CTkFrame(
            self.outputFrame,
            width=terminal_width
        )

        code_output_label = ctk.CTkLabel(
            code_output_frame,
            text=code_output,
            width=terminal_width,
            wraplength=terminal_width - 20,
            anchor="w",
            justify="left",
            font=ctk.CTkFont("Noto Sans Mono", size=11),
            bg_color="black",
            text_color="white"
        )

        code_output_label.grid(
            row=0,
            column=0,
            sticky="ns"
        )
        
        error_label = ctk.CTkLabel(
            code_output_frame,
            text=error_output,
            width=terminal_width,
            wraplength=terminal_width - 20,
            anchor="w",
            justify="left",
            font=ctk.CTkFont("Noto Sans Mono", size=11),
            bg_color="black",
            text_color="red"
        )

        error_label.grid(
            row=1,
            column=0,
            sticky="ns"
        )

        code_output_frame.grid(
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
