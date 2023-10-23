import customtkinter as ctk
from .entryForm import EntryForm
from ...std_windows.helper_class.ide import IDE
from os import path

class CodeEntryForm(EntryForm):
    def __init__(self, master, main_editor, height, width, data: tuple[str] | None=None):
        super().__init__(master, main_editor, height, width)

        self.type = "code"
        self.subwidth = self.width
        self.previous_data = data

        self.SetFrames(no_entry_adder=True)

    def SetContentFrame(self):
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure((0, 1), weight=1)

        ImportFrame = ctk.CTkFrame(self.content)
        ImportFrame.grid(row=0, column=1, padx=5, pady=5, sticky="new")

        IDEFrame = ctk.CTkFrame(self.content)
        IDEFrame.grid(row=0, column=0, padx=5, pady=5)

        nameFrame = ctk.CTkFrame(IDEFrame, corner_radius=0)
        nameFrame.grid(row=0, column=0, sticky='ew')

        nameLabel = ctk.CTkLabel(
            nameFrame,
            text='Code\'s name '
        )
        nameLabel.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.nameVar = ctk.StringVar()
        nameEntry = ctk.CTkEntry(
            nameFrame,
            textvariable=self.nameVar
        )
        nameEntry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.ide = IDE(
            IDEFrame,
            self.subwidth - 245,
            self.height,
            "tmp",
            '0',
            '.',
            None
        )
        self.set_focus_widget(self.ide)
        self.ide.grid(row=1, column=0, padx=5, pady=5)


        importCode = ctk.CTkButton(
            ImportFrame,
            text='Import Python Code From File',
            command=self.GetCodeFromFile
        )
        importCode.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        importInput = ctk.CTkButton(
            ImportFrame,
            text='Import Input File From File',
            command=self.GetInputFromFile
        )
        importInput.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        if self.previous_data is not None:
            self.error = False
            self.nameVar.set(self.previous_data[1])
            self.ide.InsertContent('0.0', self.previous_data[2], 1)
            self.ide.InsertContent('0.0', self.previous_data[3], 2)

    def GetCodeFromFile(self):
        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        file_name = path.split(file_path)[-1]
        extension = file_name.split('.')[-1]
        if len(file_name.split('.')) < 2 or extension != 'py':
            content = 'Invalid File Type, Please only import python files'
            self.error = True
            self.error_msg = 'Error in Code Entry - Invalid File Type for Code Import'
        else:
            self.nameVar.set(file_name.split('.')[0])
            with open(file_path) as file:
                content = ''.join(file.readlines())
            self.error = False

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
                    self.error = False
                except UnicodeDecodeError:
                    content = 'Invalid File Type, Please import Text Files only!'
                    self.error = True
                    self.error_msg = 'Error in Code Entry - Invalid File Type for Code Input Import'

        self.ide.ClearContent(2)
        self.ide.InsertContent("0.0", content, 2)
        self.ide.setInputFrame()
        self.ide.InputTextBox.focus()


    def getData(self):
        """returns data input into the frame in the following format
        
        (type, code name, code content, input code content)"""
        return (
            self.type,
            self.nameVar.get().strip(),
            self.ide.getCodeContent(),
            self.ide.getInputContent()
        )
