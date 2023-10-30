import customtkinter as ctk

from ...std_windows.helper_class.ide import IDE
from ...std_windows.helper_class.textboxWithPlaceholder import \
    TextBox_Placeholder
from config import DEFAULT_IDE_MESSAGE, DEFAULT_INPUT_MESSAGE


class Modified_IDE(IDE):

    """
    A heavily modifed IDE class

    Never import with Modified_IDE in testcaseEditor.py, will cause undefined
    behavior.
    """

    def __init__(self, master, content=None) -> None:
        """
        Initialises the class.
        """
        super().__init__(master, 450, 350, 'temp', '', '.', content)

        self.error = False

    def InitFrames(self):
        """
        Initialise the frames in the class.
        """

        font = ctk.CTkFont(
            "Helvetica",
            size=12,
        )

        self.idelabel = ctk.CTkLabel(
            self.left,
            text="Python Code: "
        )
        self.idelabel.grid(row=0, column=0, padx=5, pady=(5, 0), sticky='w')
        self.IDETextBox = TextBox_Placeholder(
            self.left,
            height=self.ide_height,
            font=font,
            tabs=font.measure("    "),
            wrap=ctk.WORD,
            placeholder=DEFAULT_IDE_MESSAGE
        )
        self.IDETextBox.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        if self.previous_input is not None:
            self.InsertContent("0.0", self.previous_input, 1)

        self.inputlabel = ctk.CTkLabel(
            self.right,
            text='Input List: '
        )
        self.inputlabel.grid(row=0, column=0, padx=5, pady=(5, 0), sticky='w')
        self.InputTextBox = TextBox_Placeholder(
            self.right,
            height=self.ide_height,
            font=font,
            tabs=font.measure("    "),
            wrap=ctk.WORD,
            placeholder=DEFAULT_INPUT_MESSAGE
        )
        self.InputTextBox.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    def setUpFrame(self, previous_content=None):
        """
        Setup the frames in the class.
        """

        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.left = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )
        self.left.columnconfigure(0, weight=1)
        self.left.rowconfigure(1, weight=1)
        self.left.grid(row=0, column=0, sticky='nsew')

        self.right = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )
        self.right.columnconfigure(0, weight=1)
        self.right.rowconfigure((1, 2), weight=1)
        self.right.grid(row=0, column=1, sticky='nsew')

        self.InitFrames()
        self.output_term = self.terminalOutputLabel(self.right)
        self.output_term.grid(row=2, column=0, padx=5, pady=(0, 5),
                              sticky='nsew')

        button_frame = ctk.CTkFrame(
            self.left
        )
        button_frame.columnconfigure(0, weight=1)
        button_frame.grid(row=2, column=0, padx=5, pady=5, sticky='sew')

        run_button = ctk.CTkButton(
            button_frame,
            text="Run Code",
            command=self.RunCode
        )
        run_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        import_code_button = ctk.CTkButton(
            button_frame,
            text='Import Python Code From File',
            command=self.GetCodeFromFile
        )
        import_code_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        import_input_button = ctk.CTkButton(
            button_frame,
            text='Import Input File From File',
            command=self.GetInputFromFile
        )
        import_input_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

    def display_output_terminal(self, code_output, error_output):
        """
        Display the output terminal with the output of the code.
        """

        self.output_term.configure(state='normal')
        self.output_term.delete("0.0", ctk.END)
        if code_output:
            self.insertTerminal(self.output_term, code_output, False)
        if error_output:
            self.insertTerminal(self.output_term, error_output, True)

    def GetCodeFromFile(self):
        """
        Get the code from the code file.
        """

        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        self.error = self.get_code_from_filepath(file_path, False)

    def GetInputFromFile(self):
        """
        Get the input from the input file.
        """

        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        else:
            self.error = self.get_input_from_file(file_path, False)

    def get_content(self):
        return (
            self.getCodeContent(),
            self.getInputContent()
        )

    def get_error(self):
        """
        Get potential errors if they exist.
        """

        error_list = []

        if self.getCodeContent() == '':
            error_list.append('Empty Solution')
        if self.error == True:
            if self.getCodeContent() == 'Invalid File Type, Please only import python files':
                error_list.append('Invalid File Type for Code Import')
            if self.getInputContent() == 'Invalid File Type, Please import Text Files only!':
                error_list.append('Invalid File Type for Code Input Import')

        if error_list:
            return [('Solution', error_list)]
        else:
            return []

    def import_data(self, data: tuple[str]):
        """
        Import data passed as parameter into content.
        """

        self.InsertContent('0.0', data[0], 1)
        self.InsertContent('0.0', data[1], 2)
