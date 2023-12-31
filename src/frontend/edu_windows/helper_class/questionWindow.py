from __future__ import annotations
import customtkinter as ctk

from .errorWindow import ErrorWindow
from .dataFileEditor import dataFileEditor
from .entryForm import EntryForm
from .refreshScrollFrame import RefreshableScrollableFrame


class answerframe(ctk.CTkFrame):

    """
    widget that allows the user to add and modify
    answer prompts
    """

    def __init__(self, master):
        super().__init__(master)

        self.setupframes()

    def setupframes(self):
        """
        Sets up frames in the widget
        """
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.adder_frame = ctk.CTkFrame(self)
        self.adder_frame.columnconfigure(0, weight=1)
        self.adder_frame.grid(row=0, column=0, sticky='ew')

        add_answer = ctk.CTkButton(
            self.adder_frame,
            text='Add Element',
            command=self.add_new_elem
        )
        add_answer.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.content_frame = RefreshableScrollableFrame(self)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.grid(row=1, column=0, sticky='nsew')

        self.answer_var = ctk.IntVar(value=-1)
        # self.answer_var = ctk.IntVar(value=-1)

    def add_new_elem(self):
        """
        Adds a new Answer Widget
        """
        new = answerwidget(
            self.content_frame,
            self,
            self
        )
        self.content_frame.track_element(new)
        new.SetFrames(True)
        new.focus()
        self.content_frame.refresh_elements()
        self.content_frame.scroll_frame(1)

    def get_content_data(self):
        """
        Gets data from each widget contained in the frame
        """
        return (
            self.answer_var.get(),
            [x.getData() for x in self.content_frame.get_tracking_list()]
        )

    def import_data(self, previous_content):
        """
        imports data from outer source

        each data must be formatted as such:
        (answer, [list of possible answers])
        """
        answer = previous_content[0]
        prompts = previous_content[1]
        self.answer_var.set(answer)

        for prompt in prompts:
            new = answerwidget(
                self.content_frame,
                self,
                self
            )
            self.content_frame.track_element(new)
            new.SetFrames(True)
            new.importData(prompt)
        self.content_frame.refresh_elements()
        self.content_frame.scroll_frame(0)

    def get_error_list(self):
        """
        gets list of errors from each widget contained in the frame
        """
        error_list = [x.getError() for x in self.content_frame.get_tracking_list()]
        error_msg = []

        for index, error in enumerate(error_list):
            if error:
                error_msg.append((f'Option {index + 1}', error))
        return error_msg

class answerwidget(EntryForm):
    """
    Answer Entry Widget to key in prompt
    Has a radio button for user to select the correct answer
    """
    def __init__(self, master: RefreshableScrollableFrame, parent, main_editor):
        super().__init__(master, main_editor)

        self.parent = parent

        self.type = 'Answer'

    def SetContentFrame(self):
        """
        Sets content of the frame
        """
        self.content.columnconfigure(1, weight=1)

        self.prompt = ctk.CTkTextbox(
            self.content,
            height=80
        )
        self.prompt.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.radioButton = ctk.CTkRadioButton(
            self.content,
            text='',
            variable=self.parent.answer_var,
            value=self.get_index_instance(),
            width=0,
        )
        self.radioButton.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.set_focus_widget(self.prompt)

    def grid(self, **kwargs):
        """
        Overrides the grid functionality from ctk.CtkFrame

        Now, it will first check the value of the radio button 
        if the value of the radio button is the same as the variable attached to it,
        it will set the radio button to be enabled
        and change the variable value to be the same as the new value of the radio button

        else, it remains disabled
        then it runs the default grid function

        Required to fix odd issues with radio buttons and RSF behavior of constant changing positions
        """
        # hack time
        self.radioButton._check_state = False
        if self.radioButton._variable.get() == self.radioButton._value:
            self.radioButton._variable.set(self.get_index_instance())
            self.radioButton._check_state = True
        self.radioButton._value = self.get_index_instance()
        self.radioButton._draw()

        return super().grid(**kwargs)

    def getError(self):
        """
        Get potential issues in the widget
        """
        error_list = []
        if self.prompt.get('0.0', ctk.END).strip() == '':
            error_list.append('Empty Prompt, Remove if not needed')
        return error_list

    def getData(self):
        """
        Gets data stored in the widget
        """
        return (
            self.prompt.get('0.0', ctk.END).strip()
        )

    def importData(self, data: str):
        """
        Import data from outer source

        data would be the prompt of the answer
        """
        self.prompt.insert('0.0', data)

class QuestionEditWindow(ctk.CTkToplevel):
    """
    Pop up window that allows the user to modify the content in a question,
    which are the prompt and the answer selections

    Meant to be used together with questionPreview frame
    """
    def __init__(self, master, width, height, asset_list):
        super().__init__(master)
        self.geometry(f'{width}x{height}')
        self.title(f'Editing Question')

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(1, weight=1)

        save_n_quit_button = ctk.CTkButton(
            self,
            text='Save And Quit',
            command=self.save_data
        )
        save_n_quit_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='e')

        self.file_editor = dataFileEditor(
            self,
            asset_list
        )
        self.file_editor.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.answer_editor = answerframe(self)
        self.answer_editor.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        if self.master.inner_content:
            self.file_editor.import_data_list(self.master.inner_content[0])
            self.answer_editor.import_data(self.master.inner_content[1])

    def save_data(self):
        """
        Checks for potential issues

        If there are, show a window pop up and return
        Else, save content of the class in questionPreview frame
        """
        errors = self.file_editor.get_error_list()
        errors.extend(self.answer_editor.get_error_list())

        if errors:
            error_window = ErrorWindow(self, 450, 550, errors, 'saving prompt details')
            self.winfo_toplevel().wait_window(error_window)
            return 

        self.master.inner_content = (self.file_editor.get_content_data(), self.answer_editor.get_content_data())
        self.destroy()
