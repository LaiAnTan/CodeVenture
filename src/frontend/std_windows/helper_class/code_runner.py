import os
import sys
import subprocess
import pygments as pyg
import customtkinter as ctk
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

from .imagelabel import ImageLabel
from ...ui_app import App
from config import LIGHTMODE_GRAY, DARKMODE_GRAY


class CodeRunner(ctk.CTkFrame):

    """
    Frame class that handles the display and execution of code.
    """

    def __init__(self, master, max_img_width, code_name,
                 activity_folder) -> None:
        """
        Initializes the class.
        """
        self.max_width = max_img_width

        self.code_name = code_name
        self.activity_folder = activity_folder

        self.code_folder = f"{self.activity_folder}/{self.code_name}"
        self.runnable = os.path.isfile(f'{self.code_folder}/input')

        if master is not None:
            super().__init__(master,
                             fg_color=LIGHTMODE_GRAY if
                             App().settings.getSettingValue("lightmode")
                             .lower() == "true" else DARKMODE_GRAY)

            self.rowconfigure((0, 1), weight=1)
            self.columnconfigure(0, weight=1)

            self.HeaderFrame = ctk.CTkFrame(self, fg_color='transparent')
            self.HeaderFrame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            self.CodeFrame = ctk.CTkFrame(self,
                                          fg_color='#f8f8f8' if
                                          App().settings
                                          .getSettingValue("lightmode").lower()
                                          == "true" else '#000000')
            self.CodeFrame.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

            if self.runnable:
                self.rowconfigure(2, weight=1)
                self.RunButtonFrame = ctk.CTkFrame(self,
                                                   fg_color='transparent')
                self.RunButtonFrame.grid(row=2, column=0, padx=5, pady=5)
                self.RunButtonFrame.columnconfigure(0, weight=1)

                self.outputFrame = ctk.CTkFrame(self, fg_color='black')
                self.outputFrame.columnconfigure(0, weight=1)

            self.setUpFrame()

    def DisplayCodeline_FromFile(self):
        """
        Displays the code line from a file.
        """
        with open(f"{self.code_folder}/main.py") as file:
            pyg.highlight(
                file.read(),
                PythonLexer(),
                ImageFormatter(
                    font_name="Helvetica",
                    font_size=12
                ),
                outfile=f"{self.code_folder}/temp"
            )

        ret_widget = ImageLabel(
            self.CodeFrame,
            f"{self.code_folder}/temp",
            1600,  # TODO: Change the height value later
            self.max_width,
            True
        )

        os.remove(f"{self.code_folder}/temp")

        return ret_widget

    def setUpFrame(self):
        """
        Sets up the frame.
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

        CodeContent = self.DisplayCodeline_FromFile()
        CodeContent.grid(row=0, column=0, sticky='w')

    def RunTestCases(self, testcase_path):
        """
        Runs the test cases specified in testcase_path.
        """
        cmd = [sys.executable, f'{self.code_folder}/main.py']

        testcase_in = open(testcase_path)
        try:
            code_output = subprocess.check_output(cmd, timeout=5,
                                                  stdin=testcase_in,
                                                  stderr=subprocess.STDOUT,
                                                  ).decode()
        except subprocess.CalledProcessError as errxc:
            code_output = errxc.output
        except subprocess.TimeoutExpired:
            code_output = "Timeout After Running For 5 seconds"

        return code_output

    def RunCode(self):
        """
        Runs the code specified.
        """
        for widget in self.outputFrame.winfo_children():
            widget.destroy()
        self.outputFrame.forget()

        print("Running Code.")

        cmd = [sys.executable, f'{self.code_folder}/main.py']
        code_input = open(f"{self.code_folder}/input")

        font_color = "white"
        try:
            code_output = subprocess.check_output(cmd, timeout=5,
                                                  stdin=code_input,
                                                  stderr=subprocess.STDOUT,).decode()
        except subprocess.CalledProcessError as errxc:
            code_output = errxc.output
            font_color = "red"
        except subprocess.TimeoutExpired:
            code_output = "Timeout After Running For 5 seconds"
            font_color = "red"

        placeholder = ctk.CTkLabel(
            self.outputFrame,
            text=code_output,
            anchor="w",
            justify="left",
            font=("Helvetica", 11),
            bg_color="black",
            text_color=font_color
        )
        placeholder.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.outputFrame.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
