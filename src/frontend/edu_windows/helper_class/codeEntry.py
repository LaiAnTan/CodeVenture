import customtkinter as ctk
from .entryForm import EntryForm
from ...std_windows.helper_class.ide import IDE
from os import path

class CodeEntryForm(EntryForm):
    """
    Allow user to create code snippet by typing
    out the code snippet or importing from 
    already existing python files
    """
    def __init__(self, master, main_editor):
        super().__init__(master, main_editor)

        self.type = "code"

        self.error = False
        self.error_msg = ''

        self.SetFrames(no_entry_adder=True)

    def SetContentFrame(self):
        """
        Sets content frame of the widget
        """
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=70)
        self.content.columnconfigure(1, weight=30)

        ImportFrame = ctk.CTkFrame(self.content, fg_color='transparent')
        ImportFrame.columnconfigure(0, weight=1)
        ImportFrame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        IDEFrame = ctk.CTkFrame(self.content, fg_color='transparent')
        IDEFrame.columnconfigure(0, weight=1)
        IDEFrame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        nameFrame = ctk.CTkFrame(IDEFrame, corner_radius=0, fg_color='transparent')
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
            250,
            100,
            "tmp",
            '0',
            '.',
            None
        )
        self.set_focus_widget(self.ide)
        self.ide.grid(row=1, column=0, sticky='ew')


        importCode = ctk.CTkButton(
            ImportFrame,
            text='Import Python Code From File',
            command=self.GetCodeFromFile,
            width=0
        )
        importCode.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        importInput = ctk.CTkButton(
            ImportFrame,
            text='Import Input File From File',
            command=self.GetInputFromFile,
            width=0
        )
        importInput.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.runnable_var = ctk.BooleanVar(value=True)
        runnable = ctk.CTkSwitch(
            ImportFrame,
            text='Runnable',
            onvalue=True,
            offvalue=False,
            variable=self.runnable_var
        )
        runnable.grid(row=2, column=0, padx=5, pady=5)

    def GetCodeFromFile(self):
        """
        Displays a prompt to choose a file from

        Then extracts the content of the python file and 
        places them into the IDE entry form

        error flag is set if file imported is invalid, or
        file attempted to import doesnt exist
        """
        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        self.error = self.ide.get_code_from_filepath(file_path)
        if self.error != True:
            name = path.split(file_path)[-1]
            self.nameVar.set(name.split('.')[0])

    def GetInputFromFile(self):
        """
        Displays a prompt to choose a file from

        Then extracts the content of the python file and 
        places them into the Input entry form to be used
        as code input

        error flag is set if file imported is invalid, or
        file attempted to import doesnt exist
        """
        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        else:
            self.error = self.ide.get_input_from_file(file_path)

    def getData(self):
        """returns data input into the frame in the following format
        
        (type, code name, code content, input code content)"""
        return (
            self.type,
            self.nameVar.get().strip(),
            self.ide.getCodeContent(),
            self.ide.getInputContent() if self.runnable_var.get() is True else None
        )

    def getError(self):
        """
        returns a list of errors that may have occured within the widget

        error returned in the format of a list of strings
        """
        errorlist = []

        if self.ide.getCodeContent() == "" and self.nameVar.get().strip() == '':
            errorlist.append('Entry Frame is left unused, Remove if not needed')
        else:
            if self.nameVar.get().strip() == '':
                errorlist.append('Name not given')

            if self.error == True:
                if self.ide.getCodeContent() == 'Invalid File Type, Please only import python files':
                    errorlist.append('Invalid File Type for Code Import')
                if self.ide.getInputContent() == 'Invalid File Type, Please import Text Files only!':
                    errorlist.append('Invalid File Type for Code Input Import')

        return errorlist

    def importData(self, data: tuple[str]):
        """
        imports existing data into the widget

        data must be in the following format
        ('code', name, code content, input content (None if is unrunnable))
        """
        if data[0] != 'code':
            assert AssertionError("Wrong Type")

        super().importData(data)
        self.nameVar.set(data[1])

        self.ide.ClearContent(1)
        self.ide.InsertContent("0.0", data[2], 1)

        if data[3] != None:
            self.ide.ClearContent(2)
            self.ide.InsertContent("0.0", data[3], 2)
        else:
            self.runnable_var.set(False)

        self.ide.setCodeFrame()