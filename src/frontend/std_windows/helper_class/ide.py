import os
import sys

import customtkinter as ctk

import subprocess

from .textboxWithPlaceholder import TextBox_Placeholder
from config import DEFAULT_IDE_MESSAGE, DEFAULT_INPUT_MESSAGE


class IDE(ctk.CTkFrame):

    """
    Class that represents an IDE frame.
    """

    def __init__(self, master, width, height, code_name, id, activity_folder,
                 content=None) -> None:
        super().__init__(master)

        self.max_width = width
        self.max_height = height
        self.terminal_width = self.max_width - 5

        self.code_name = f"{code_name}-{id}"
        self.activity_folder = activity_folder

        self.max_output_size = 45000

        # fuck, max output size can change :'D
        # self.max_output_size = 65000
        self.previous_input = content

        # please change this to a reasonable timeout period
        self.timeout_period = 10

        self.IDEHeader = ctk.CTkFrame(self, width=self.max_width)
        self.IDEHeader.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.IDEContent = ctk.CTkFrame(self, width=self.max_width)
        self.IDEContent.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.outputFrame = ctk.CTkFrame(self)

        self.setUpFrame()

    def ClearContent(self, which):
        """
        Function that clears the content of either one of the textboxes.

        set which to 1 if want to clear to IDE's TextBox

        set which to 2 if want to clear to Input's TextBox
        """
        if which == 1:
            self.IDETextBox.delete("0.0", ctk.END)
        elif which == 2:
            self.InputTextBox.delete("0.0", ctk.END)

    def InsertContent(self, index, content, which):
        """
        Function that inserts content into either one of the textboxes.

        set which to 1 if want to insert to IDE's TextBox

        set which to 2 if want to insert to Input's TextBox
        """
        if which == 1:
            self.IDETextBox.insert(index, content)
        elif which == 2:
            self.InputTextBox.insert(index, content)

    def InitIDEWindow(self):
        """
        Function that initialises the IDE frame.
        """
        font = ctk.CTkFont(
            "Helvetica",
            size=12,
        )

        self.IDETextBox = TextBox_Placeholder(
            self.IDEContent,
            width=self.max_width,
            height=self.max_height,
            font=font,
            tabs=font.measure("    "),
            wrap=ctk.WORD,
            placeholder=DEFAULT_IDE_MESSAGE
        )

        if self.previous_input is not None:
            self.InsertContent("0.0", self.previous_input, 1)

    def InitInputFrame(self):
        """
        Function that initialises the input frame.
        """
        font = ctk.CTkFont(
            "Helvetica",
            size=12,
        )

        self.InputTextBox = TextBox_Placeholder(
            self.IDEContent,
            width=self.max_width,
            height=self.max_height,
            font=font,
            tabs=font.measure("    "),
            wrap=ctk.WORD,
            placeholder=DEFAULT_INPUT_MESSAGE
        )

    def setInputFrame(self):
        """
        Function that attaches the input frame.
        """
        self.IDETextBox.grid_forget()
        self.InputTextBox.grid(row=0, column=0, padx=5, pady=5)
        self.InputTextBox.focus()

    def setCodeFrame(self):
        """
        Function that attaches the IDE frame.
        """
        self.InputTextBox.grid_forget()
        self.IDETextBox.grid(row=0, column=0, padx=5, pady=5)
        self.IDETextBox.focus()

    def setUpFrame(self):
        """
        Function that performs attachment of main elements onto the main
        frame.
        """
        self.IDEHeader.rowconfigure((0, 1), weight=1)
        self.IDEHeader.columnconfigure((0, 1), weight=1)

        CodeButton = ctk.CTkButton(
            self.IDEHeader,
            text="Code",
            command=self.setCodeFrame
        )
        CodeButton.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        InputButton = ctk.CTkButton(
            self.IDEHeader,
            text="Input",
            command=self.setInputFrame
        )
        InputButton.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.InitIDEWindow()
        self.InitInputFrame()
        self.setCodeFrame()

        RunButton = ctk.CTkButton(
            self.IDEContent,
            text="Run",
            command=self.RunCode,
            height=10
        )
        RunButton.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    def getCodeContent(self):
        """
        Getter for IDE text box content.
        """
        return self.IDETextBox.get("0.0", "end").strip()

    def getInputContent(self):
        """
        Getter for input text box content.
        """
        return self.InputTextBox.get("0.0", "end").strip()

    def RunTestCases(self, testcases):
        """
        Function that runs all test cases.
        """
        # open file and dump all data inside
        text = self.IDETextBox.get("0.0", "end")
        testcase_in = open(f"{self.activity_folder}/{testcases}")

        with open(f"{self.activity_folder}/{self.code_name}", "w") as file:
            file.write(text)

        cmd = f"{sys.executable} \"{self.activity_folder}/{self.code_name}\""

        try:
            code_output = subprocess.check_output(cmd, timeout=10,
                                                  stdin=testcase_in,
                                                  stderr=subprocess.STDOUT,
                                                  shell=True).decode()
        except subprocess.CalledProcessError as errxc:
            code_output = errxc.output
        except subprocess.TimeoutExpired:
            code_output = "Timeout After Running For 10 seconds"

        # remove the file
        os.remove(f"{self.activity_folder}/{self.code_name}")

        # Returns the output
        # if error, return the raw error output
        return code_output

    def terminalOutputLabel(self, output, attach_to, max_width, word_color):
        """
        Function that attaches the output of the code to the frame attach_to.
        """
        output = output[:self.max_output_size]
        output_label = ctk.CTkLabel(
            attach_to,
            text=output,
            width=max_width,
            wraplength=max_width,
            anchor="w",
            justify="left",
            font=ctk.CTkFont("Helvetica", size=11),
            bg_color="black",
            text_color=word_color
        )
        return output_label

    def RunCode(self):
        """
        Function that runs the code that was written in the IDE text box,
        with potential inputs from the input text box.
        """
        for widget in self.outputFrame.winfo_children():
            widget.destroy()
        self.outputFrame.forget()

        print("Running Code.")

        # open file and dump all data inside
        text = self.IDETextBox.get("0.0", "end")
        with open(f"{self.activity_folder}/{self.code_name}", "w") as file:
            file.write(text)

        cmd = f"{sys.executable} \"{self.activity_folder}/{self.code_name}\""

        user_input = self.InputTextBox.get("0.0", "end")
        user_input = bytes(user_input, "utf-8")
        try:
            code_runner = subprocess.run(cmd, timeout=10, input=user_input,
                                         capture_output=True, shell=True)
            code_output = code_runner.stdout
            error_output = code_runner.stderr
        except subprocess.TimeoutExpired:
            code_output = bytes("", "utf-8")
            error_output = bytes("Timeout After Running For 10 seconds",
                                 "utf-8")

        # remove the file
        os.remove(f"{self.activity_folder}/{self.code_name}")

        if code_output or error_output:
            code_output_frame = ctk.CTkFrame(self.outputFrame)
            code_output_frame.grid(row=0, column=0, padx=5, pady=5)
            self.outputFrame.grid(row=3, column=0, padx=5, pady=5)

            if code_output:
                code_output_label = self.terminalOutputLabel(code_output,
                                                             code_output_frame,
                                                             self.terminal_width,
                                                             "white")
                code_output_label.grid(row=0, column=0, sticky="ns")

            if error_output:
                error_label = self.terminalOutputLabel(error_output,
                                                       code_output_frame,
                                                       self.terminal_width,
                                                       "red")
                error_label.grid(row=1, column=0, sticky="ns")
