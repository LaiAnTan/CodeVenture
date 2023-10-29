"""
Like Code Entry, but not really LIKE code entry yeah?
"""

import customtkinter as ctk

from ...std_windows.helper_class.ide import IDE
from ...std_windows.helper_class.textboxWithPlaceholder import TextBox_Placeholder
from config import DEFAULT_IDE_MESSAGE, DEFAULT_INPUT_MESSAGE

class Modified_IDE(IDE):
    """
    A heavily modifed IDE class
    """
    def __init__(self, master, content = None) -> None:
        super().__init__(master, 450, 350, 'temp', '', '.', content)

        self.error = False
        self.error_msg = ''

    def InitFrames(self):
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
        Overriden
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
        self.output_term.grid(row=2, column=0, padx=5, pady=(0, 5), sticky='nsew')

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
        Overriden
        """
        self.output_term.configure(state='normal')
        self.output_term.delete("0.0", ctk.END)
        if code_output:
            self.insertTerminal(self.output_term, code_output, False)
        if error_output:
            self.insertTerminal(self.output_term, error_output, True)

    def GetCodeFromFile(self):
        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        self.error, self.error_msg = self.get_code_from_filepath(file_path, False)

    def GetInputFromFile(self):
        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        else:
            self.error, self.error_msg = self.get_input_from_file(file_path, False)

    def get_content(self):
        return (
            self.getCodeContent(),
            self.getInputContent()
        )
    
    def get_error(self):
        if self.getCodeContent() == '':
            return [(
                'Solution',
                'Empty Solution'
            )]

        return [('Solution', self.error_msg)] if self.error is True else []
