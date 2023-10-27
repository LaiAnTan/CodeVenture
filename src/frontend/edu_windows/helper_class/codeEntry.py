import customtkinter as ctk
from .entryForm import EntryForm
from ...std_windows.helper_class.ide import IDE
from os import path

class CodeEntryForm(EntryForm):
    def __init__(self, master, main_editor, data: tuple[str] | None=None):
        super().__init__(master, main_editor)

        self.type = "code"
        self.previous_data = data

        self.error = False
        self.error_msg = ''

        self.SetFrames(no_entry_adder=True)

    def SetContentFrame(self):
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=70)
        self.content.columnconfigure(1, weight=30)
        # self.content.columnconfigure((0, 1), weight=1)

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

        if self.previous_data is not None:
            self.error = False
            self.nameVar.set(self.previous_data[1])
            self.ide.InsertContent('0.0', self.previous_data[2], 1)
            self.ide.InsertContent('0.0', self.previous_data[3], 2)

    def GetCodeFromFile(self):
        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        self.error, self.error_msg = self.ide.get_code_from_filepath(file_path)
        if self.error != True:
            name = path.split(file_path)[-1]
            self.nameVar.set(name.split('.')[0])

    def GetInputFromFile(self):
        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        else:
            self.error, self.error_msg = self.ide.get_input_from_file(file_path)

    def getData(self):
        """returns data input into the frame in the following format
        
        (type, code name, code content, input code content)"""
        return (
            self.type,
            self.nameVar.get().strip(),
            self.ide.getCodeContent(),
            self.ide.getInputContent()
        )

    def getError(self):
        if self.ide.getCodeContent() == "":
            return (
                True,
                'Entry Frame is left unused, Remove if not needed'
            )
        return super().getError()