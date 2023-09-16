import pygments as pyg
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

from PIL import Image
from PIL.ImageOps import invert

import os
import sys

import customtkinter as ctk

import subprocess
import select

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

        self.IDEFrame.grid(
            row=0,
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

    def this_shitting_thing(self, input_frame, terminal_width):
        cmd = [sys.executable, f"{self.root_path}{self.code_name}"]

        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.set_blocking(proc.stdout.fileno(), False)
        os.set_blocking(proc.stderr.fileno(), False)

        ## time to snort cocain
        def remove_and_send(eventfo):
            out = input_frame.get()
            input_frame.delete(0, ctk.END)
            try:
                proc.communicate(input=bytes(out.strip(), "utf-8"))
            except ValueError:
                print("I spent too much time on this...")
            
            ## https://stackoverflow.com/questions/65874314/how-to-remove-blank-line-at-end-of-tkinter-textbox  fasinating
            return "break"

        input_frame.bind(
            "<KeyPress-Return>",
            command=remove_and_send
        )

        # i am epic distorting

        # frame_count = 1
        # while True:
        #     output = proc.stdout.readline()
        #     error = proc.stderr.readline()

        #     if proc.poll() is not None and not output and not error:
        #         break

        #     if output or error:
        #         print(f"output = {output}, error = {error}")

        #     if output:
        #         code_output_label = self.create_label(output, terminal_width, "white")
        #         code_output_label.grid( row=frame_count, column=0 )
        #         frame_count += 1
        #     if error:
        #         error_label = self.create_label(error, terminal_width, "red")
        #         error_label.grid( row=frame_count, column=0 )
        #         frame_count += 1

        ## remove the file
        os.remove(f"{self.root_path}{self.code_name}")

    def RunCode(self):
        for widget in self.outputFrame.winfo_children():
            widget.destroy()
        self.outputFrame.forget()

        terminal_width = (self.max_width - 50)

        ## open file and dump all data inside
        text = self.IDETextBox.get("0.0", "end")
        with open(f"{self.root_path}{self.code_name}", "w") as file:
            file.write(text)

        self.outputFrame.grid(
            row=3,
            column=0,
            padx=5,
            pady=5
        )

        input_frame = ctk.CTkEntry(
            self.outputFrame,
            placeholder_text="Input Goes here"
        )

        input_frame.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.this_shitting_thing(input_frame, terminal_width)

    def create_label(self, content, max_width, color):
        ret = ctk.CTkLabel(
            self.outputFrame,
            text=content,
            width=max_width,
            wraplength=max_width - 20,
            height=15,
            anchor="w",
            justify="left",
            font=ctk.CTkFont("Noto Sans Mono", size=11),
            bg_color="black",
            text_color=color
        )
        
        return ret