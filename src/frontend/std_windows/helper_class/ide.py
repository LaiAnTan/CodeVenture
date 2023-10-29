import os
import sys

import customtkinter as ctk

import subprocess

from .textboxWithPlaceholder import TextBox_Placeholder
from config import DEFAULT_IDE_MESSAGE, DEFAULT_INPUT_MESSAGE

class IDE(ctk.CTkFrame):
    def __init__(self, master, ide_height, output_height, code_name, id, activity_folder, content=None) -> None:
        super().__init__(master, fg_color='transparent')

        self.ide_height = ide_height
        self.max_term_height = output_height

        self.code_name = f"{code_name}-{id}"
        self.activity_folder = activity_folder

        self.max_output_size = 45000

        # fuck, max output size can change :'D
        # self.max_output_size = 65000
        self.previous_input = content

        ## please change this to a reasonable timeout period
        self.timeout_period = 10

        self.setUpFrame()

    def ClearContent(self, which):
        """set which to 1 if want to clear to IDE's TextBox

        set which to 2 if want to clear to Input's TextBox"""
        if which == 1:
            self.IDETextBox.delete("0.0", ctk.END)
        elif which == 2:
            self.InputTextBox.delete("0.0", ctk.END)


    def InsertContent(self, index, content, which):
        """set which to 1 if want to insert to IDE's TextBox

        set which to 2 if want to insert to Input's TextBox"""
        if which == 1:
            self.IDETextBox.insert(index, content)
        elif which == 2:
            self.InputTextBox.insert(index, content)

    def InitIDEWindow(self):
        font = ctk.CTkFont(
            "Helvetica",
            size=12,
        )

        self.IDETextBox = TextBox_Placeholder(
            self.IDEContent,
            height=self.ide_height,
            font=font,
            tabs=font.measure("    "),
            wrap=ctk.WORD,
            placeholder=DEFAULT_IDE_MESSAGE
        )

        if self.previous_input is not None:
            self.InsertContent("0.0", self.previous_input, 1)

    def InitInputFrame(self):
        font = ctk.CTkFont(
            "Helvetica",
            size=12,
        )

        self.InputTextBox = TextBox_Placeholder(
            self.IDEContent,
            height=self.ide_height,
            font=font,
            tabs=font.measure("    "),
            wrap=ctk.WORD,
            placeholder=DEFAULT_INPUT_MESSAGE
        )

    def setInputFrame(self):
        self.IDETextBox.grid_forget()
        self.InputTextBox.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.InputTextBox.focus()
        
    def setCodeFrame(self):
        self.InputTextBox.grid_forget()
        self.IDETextBox.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.IDETextBox.focus()

    def	setUpFrame(self, previous_content = None):
        self.columnconfigure(0, weight=1)

        self.IDEHeader = ctk.CTkFrame(self)
        self.IDEHeader.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        self.IDEContent = ctk.CTkFrame(self)
        self.IDEContent.columnconfigure(0, weight=1)
        self.IDEContent.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.outputFrame = ctk.CTkFrame(self, fg_color='black')
        self.outputFrame.columnconfigure(0, weight=1)

        self.terminal = self.terminalOutputLabel(self.outputFrame)
        self.terminal.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.IDEHeader.rowconfigure((0,1), weight=1)
        self.IDEHeader.columnconfigure((0,1), weight=1)

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
        return self.IDETextBox.get("0.0", "end").strip()

    def getInputContent(self):
        return self.InputTextBox.get("0.0", "end").strip()

    def RunTestCases(self, testcases):
        ## open file and dump all data inside
        text = self.IDETextBox.get("0.0", "end")
        testcase_in = open(f"{self.activity_folder}/{testcases}")

        with open(f"{self.activity_folder}/{self.code_name}", "w") as file:
            file.write(text)

        cmd = f"{sys.executable} \"{self.activity_folder}/{self.code_name}\""

        try:
            code_output = subprocess.check_output(cmd, timeout=10, stdin=testcase_in, stderr=subprocess.STDOUT, shell=True).decode()
        except subprocess.CalledProcessError as errxc:
            code_output = errxc.output
        except subprocess.TimeoutExpired:
            code_output = "Timeout After Running For 10 seconds"

        ## remove the file
        os.remove(f"{self.activity_folder}/{self.code_name}")

        ## Returns the output
        ## if error, return the raw error output
        return code_output

    def terminalOutputLabel(self, attach_to):
        output_label = ctk.CTkTextbox(
            attach_to,
            font=ctk.CTkFont("Helvetica", size=12),
            fg_color='black',
            height=self.max_term_height,
            wrap='word',
            state='disabled'
        )
        output_label.tag_config("normal", foreground='white')
        output_label.tag_config("error", foreground='red')
        return output_label


    def insertTerminal(self, terminal: ctk.CTkTextbox, content, error):
        content = content[:self.max_output_size]
        last_post = terminal.index(ctk.CURRENT)
        terminal.configure(state='normal')
        terminal.insert(last_post, content)
        terminal.configure(state='disabled')

        if error:
            terminal.tag_add("error", last_post, ctk.END)
        else:
            terminal.tag_add("normal", last_post, ctk.END)


    def RunCode(self):
        print("Running Code. BzzZt")

        ## open file and dump all data inside
        text = self.IDETextBox.get("0.0", "end")
        with open(f"{self.activity_folder}/{self.code_name}", "w") as file:
            file.write(text)

        # run code
        cmd = f"{sys.executable} \"{self.activity_folder}/{self.code_name}\""

        user_input = self.InputTextBox.get("0.0", "end")
        user_input = bytes(user_input, "utf-8")
        try:
            code_runner = subprocess.run(cmd, 
                                         timeout=10, 
                                         input=user_input, 
                                         capture_output=True, 
                                         shell=True)
            code_output = code_runner.stdout
            error_output = code_runner.stderr
        except subprocess.TimeoutExpired as err:    
            code_output = err.stdout.decode() if err.stdout is not None else '' # does not work for some reason, god hates me
            error_output = bytes("Timeout After Running For 10 seconds", "utf-8")

        ## remove the file
        os.remove(f"{self.activity_folder}/{self.code_name}")
        self.display_output_terminal(code_output, error_output)

    def display_output_terminal(self, code_output, error_output):
        self.terminal.configure(state='normal')
        self.terminal.delete('0.0', ctk.END)

        if code_output or error_output:
            self.outputFrame.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
            if code_output:
                self.insertTerminal(self.terminal, code_output, False)
            if error_output:
                self.insertTerminal(self.terminal, error_output, True)
            self.terminal.configure(state='disabled')
        else:
            self.outputFrame.grid_forget()

    # used in code entry and nowhere else

    def get_code_from_filepath(self, filepath, switch= True):
        """
        probably shhhouldd have placed it here in the first place
        """
        return_val = (False, '')
        file_name = os.path.split(filepath)[-1]
        extension = file_name.split('.')[-1]
        if len(file_name.split('.')) < 2 or extension != 'py':
            content = 'Invalid File Type, Please only import python files'
            return_val = (True, 'Error in code entry - Invalid File Type')
        else:
            with open(filepath) as file:
                content = ''.join(file.readlines())

        self.ClearContent(1)
        self.InsertContent("0.0", content, 1)
        self.IDETextBox.focus()
        if switch:
            self.setCodeFrame()
        return return_val

    def get_input_from_file(self, filepath, switch= True):
        return_val = (False, '')
        with open(filepath) as file:
            try:
                content = ''.join(file.readlines())
            except UnicodeDecodeError:
                content = 'Invalid File Type, Please import Text Files only!'
                return_val = (True, 'Error in Code Entry - Invalid File Type for Code Input Import')

        self.ClearContent(2)
        self.InsertContent("0.0", content, 2)
        self.InputTextBox.focus()
        if switch:
            self.setInputFrame()
        return return_val