from .refreshScrollFrame import RefreshableScrollableFrame
from .entryForm import EntryForm
import customtkinter as ctk
from ...std_windows.helper_class.ide import IDE, TextBox_Placeholder, DEFAULT_INPUT_MESSAGE

class Modified_IDE(IDE):
    """
    you did not modify ide again YES I DID BABYYY
    """
    def __init__(self, master, editor):
        super().__init__(master, 180, 240, 'temp', '', '.', None)

        self.editor = editor

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
        self.right.rowconfigure(1, weight=1)
        self.right.grid(row=0, column=1, sticky='nsew')

        self.InitFrames()

        output_label = ctk.CTkLabel(
            self.right,
            text='Solution\'s Output With Provided Input: ',
        )
        output_label.grid(row=0, column=0, padx=5, sticky='w')
        self.output_term = self.terminalOutputLabel(self.right)
        self.output_term.grid(row=1, column=0, padx=5, sticky='nsew')

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

        import_input_button = ctk.CTkButton(
            button_frame,
            text='Import Input File From File',
            command=self.GetInputFromFile
        )
        import_input_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')


    def InitFrames(self):
        font = ctk.CTkFont(
            "Helvetica",
            size=12,
        )

        # the default textbox would be sufficient here
        self.IDETextBox = ctk.CTkTextbox(self.left)

        inputlabel = ctk.CTkLabel(
            self.left,
            text='Input List: '
        )
        inputlabel.grid(row=0, column=0, padx=5, pady=(5, 0), sticky='w')
        self.InputTextBox = TextBox_Placeholder(
            self.left,
            height=self.ide_height,
            font=font,
            tabs=font.measure("    "),
            wrap=ctk.WORD,
            placeholder=DEFAULT_INPUT_MESSAGE
        )
        self.InputTextBox.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')


    def GetInputFromFile(self):
        file_path = ctk.filedialog.askopenfilename()
        if not file_path:
            return
        else:
            self.error, self.error_msg = self.get_input_from_file(file_path, False)


    def RunCode(self):
        solution_code = self.editor.solution.getCodeContent()
        self.IDETextBox.delete('0.0', ctk.END)
        self.IDETextBox.insert('0.0', solution_code)
        return super().RunCode()


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


    def import_data(self, data: str):
        self.InsertContent('0.0', data, 2)


class testCaseFrame(EntryForm):
    def __init__(self, master, editor):
        super().__init__(master, editor)
        self.type = 'Test Case'

        self.editor = editor
        self.SetFrames(True)

    def getData(self):
        return self.ide.getInputContent()

    def getError(self):
        return []
    
    def SetContentFrame(self):
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        self.ide = Modified_IDE(self.content, self.editor)
        self.set_focus_widget(self.ide.InputTextBox)
        self.ide.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def importData(self, data: str):
        self.ide.import_data(data)


class testCaseEditor(ctk.CTkFrame):
    def __init__(self, master, editor):
        super().__init__(master)
        self.editor = editor
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.add_more_button = ctk.CTkButton(
            self,
            text='Add a Test Case',
            command=self.add_a_test_case
        )
        self.add_more_button.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.testcase_frame = RefreshableScrollableFrame(
            self
        )
        self.testcase_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    def add_a_test_case(self):
        new = testCaseFrame(
            self.testcase_frame,
            self.editor
        )
        self.testcase_frame.track_element(new)
        self.testcase_frame.refresh_elements()
        new.focus()
        self.testcase_frame.scroll_frame(1)

        return new

    def import_data(self, data_list):
        for data in data_list:
            frame = self.add_a_test_case()
            frame.importData(data)

    def get_content_data(self):
        return [x.getData() for x in self.testcase_frame.get_tracking_list()]

    def get_error_list(self):
        error_list = []
        if self.get_content_data() == []:
            error_list.append(('Test Case', ['No Test Case Provided']))

        return error_list