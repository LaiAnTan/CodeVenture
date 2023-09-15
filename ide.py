import pygments as pyg
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

from PIL import Image
from PIL.ImageOps import invert

import os
import sys

import customtkinter as ctk

import subprocess

class IDE():
	def __init__(self, max_img_width, attach_frame, code_name, id, root_path) -> None:
		self.max_width = max_img_width
		self.attach_frame = attach_frame
		self.code_name = f"{code_name}-{id}"
		self.root_path = root_path

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
			height=360,
			font=font,
			tabs=font.measure("    ")
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

		CodeContent = self.setUpIDEWindow()

		CodeContent.grid(
			row=0,
			column=0,
			padx=5,
			pady=5
		)

		self.IDEFrame.grid(
			row=0,
			column=0,
			padx=5,
			pady=5,
		)

		self.RunButtonFrame.grid(
			row=1,
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

		print("Running Code. BzzZt")

		## open file and dump all data inside
		text = self.IDETextBox.get("0.0", "end")
		with open(f"{self.root_path}{self.code_name}", "w") as file:
			file.write(text)

		cmd = f"{sys.executable} {self.root_path}{self.code_name}"
		font_color = "white"
		try:
			code_output = subprocess.check_output(cmd, timeout=10, stderr=subprocess.STDOUT, shell=True)
		except subprocess.CalledProcessError as errxc:
			code_output = errxc.output
			font_color = "red"
		except subprocess.TimeoutExpired:
			code_output = "Timeout After Running For 10 seconds"
			font_color = "red"

		## remove the file
		os.remove(f"{self.root_path}{self.code_name}")
		code_output.decode()

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
			row=2,
			column=0,
			padx=5,
			pady=5
		)
