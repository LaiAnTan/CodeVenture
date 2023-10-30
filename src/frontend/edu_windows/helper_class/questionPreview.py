import customtkinter as ctk

from .entryForm import EntryForm
from .refreshScrollFrame import RefreshableScrollableFrame
from .questionWindow import QuestionEditWindow
from .dataFileEditor import dataFileEditor

class QuestionPreview(EntryForm):
    def __init__(self, master: RefreshableScrollableFrame, main_editor):
        super().__init__(master, main_editor)

        self.type = 'Question'

        self.assets = main_editor.asset
        self.inner_content = ([], (-1, []))

        self.SetFrames(True)


    def swap_up(self):
        index = self.get_index_instance()
        if index == 0:
            return
        self.parent_frame.swap_order(index, index - 1)
        self.parent_frame.refresh_elements()


    def swap_down(self):
        index = self.get_index_instance()
        if index == (self.master.get_tracking_no() - 1):
            return
        self.parent_frame.swap_order(index, index + 1)
        self.parent_frame.refresh_elements()


    def SetContentFrame(self):
        self.content.columnconfigure(0, weight=1)

        buttons = ctk.CTkFrame(self.content)
        buttons.columnconfigure(0, weight=10)
        buttons.columnconfigure(1, weight=80)
        buttons.columnconfigure(2, weight=10)
        buttons.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        bring_up = ctk.CTkButton(
            buttons,
            text='▲',
            width=0,
            command=self.swap_up
        )
        bring_up.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        edit_button = ctk.CTkButton(
            buttons,
            text='Edit Question',
            width=0,
            command=self.editor_window
        )
        edit_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.set_focus_widget(edit_button)

        bring_down = ctk.CTkButton(
            buttons,
            text='▼',
            width=0,
            command=self.swap_down
        )
        bring_down.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        preview = ctk.CTkFrame(self.content)
        preview.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        preview.columnconfigure(0, weight=1)

        # no, this will only print out the first line of content which is also trunicated
        self.displaying_preview = ctk.StringVar(value='Nothing here, place some content in \'Edit Question\'')
        preview_label = ctk.CTkLabel(
            preview,
            textvariable=self.displaying_preview
        )
        preview_label.grid(row=0, column=0)

    def editor_window(self):
        editor_window = QuestionEditWindow(self, 1350, 720, self.main_editor.asset)
        self.winfo_toplevel().wait_window(editor_window)

        # get the description
        self.__get_description()


    def __get_description(self):
        found = False
        prompt = self.inner_content[0]
        if prompt:
            for content in prompt:
                if content[0] == 'paragraph':
                    found = True
                    self.displaying_preview.set(content[1][:60]) # TODO: change that 50 to idk lol
                    break
            if found is False:
                self.displaying_preview.set(f'This question has {prompt[0][1][0]} assets')
        else:
            self.displaying_preview.set('Nothing here, place some content in \'Edit Question\'')


    def importData(self, data: tuple[str]):
        # data parameter will be in the following format
        # (prompt data, (answer, option list))
        self.inner_content = data
        self.__get_description()


    def getError(self):
        error_list = []

        if not self.inner_content[0]:
            return ['Empty Question, remove if not needed']

        checker = dataFileEditor(self, self.assets)
        checker.import_data_list(self.inner_content[0])

        error_list = checker.get_error_list()
        if error_list:
            error_list.append('There is an issue with this question, check question content')
        checker.destroy()

        if not self.inner_content[1][1]:
            error_list.append('No options for question')

        if self.inner_content[1][0] == -1:
            error_list.append('No answer for question')

        return error_list


    def getData(self):
        return self.inner_content
