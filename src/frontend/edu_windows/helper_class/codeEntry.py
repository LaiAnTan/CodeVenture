import customtkinter as ctk
from .EntryForm import EntryForm
from ...std_windows.helper_class.ide import IDE
from os import path

class CodeEntryForm(EntryForm):
    def __init__(self, master, parent, height, width):
        super().__init__(master, parent, height, width)

        self.type = "code"
        self.subwidth = self.width

        self.SetFrames()

    def SetContent(self):
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure((0, 1), weight=1)

        self.ImportFrame = ctk.CTkFrame(self.content)
        self.ImportFrame.grid(row=0, column=1, padx=5, pady=5, sticky="new")

        self.ide = IDE(
            self.content,
            self.subwidth - 245,
            self.height,
            "tmp",
            '0',
            '.',
            None
        )
        self.ide.grid(row=0, column=0, padx=5, pady=5)

        self.ContentEntryForm = self.ide.IDETextBox

        importCode = ctk.CTkButton(
            self.ImportFrame,
            text='Import Python Code From File',
            command=self.GetCodeFromFile
        )
        importCode.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        importInput = ctk.CTkButton(
            self.ImportFrame,
            text='Import Input File From File',
            command=self.GetInputFromFile
        )
        importInput.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

    def GetCodeFromFile(self):
        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        file_name = path.split(file_path)[-1]
        extension = file_name.split('.')[-1]
        if len(file_name.split('.')) < 2 or extension != 'py':
            content = 'Invalid File Type'
        else:
            with open(file_path) as file:
                content = ''.join(file.readlines())

        self.ide.ClearContent(1)
        self.ide.InsertContent("0.0", content, 1)
        self.ide.setCodeFrame()
        self.ide.IDETextBox.focus()


    def GetInputFromFile(self):
        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        else:
            with open(file_path) as file:
                try:
                    content = ''.join(file.readlines())
                except UnicodeDecodeError:
                    content = 'Invalid File Type, Please Input Text Files only!'

        self.ide.ClearContent(2)
        self.ide.InsertContent("0.0", content, 2)
        self.ide.setInputFrame()
        self.ide.InputTextBox.focus()