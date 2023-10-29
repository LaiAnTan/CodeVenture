"""
mfw label has no wrap text
and i need to come out one myself
"""

import customtkinter as ctk
from ...ui_app import App


# i cannot start to emphasize how laggy this was

# class to_kill_a_mockingbird(ctk.CTkTextbox):
#     def __init__(self, master):
#         self.const_height = 1
#         super().__init__(master=master, height=self.const_height, wrap='word', fg_color='transparent')
#         self.init = True

#     def grid(self, **kwargs):
#         self.init = True
#         super().grid(**kwargs)

#     def _check_if_scrollbars_needed(self, event=None, continue_loop: bool = False):
#         # print(self._textbox.yview())
#         if self.init:
#             self.update() # shouldnt need to call update() but here we are, amen
#             while self._textbox.yview()[1] < 1:
#                 hidden_away = 1 - self._textbox.yview()[1]
#                 new_height = (self.const_height) * (hidden_away + 1)
#                 self.configure(height=new_height) # amen
#                 self.const_height = new_height
#             self.init = False
#         super()._check_if_scrollbars_needed(event, continue_loop)

# class ParagraphDisplayer(ctk.CTkFrame):
#     def __init__(self, master: any, content: str):
#         super().__init__(master, fg_color='transparent')
#         self.columnconfigure(0, weight=1)

#         self._innertextbox = to_kill_a_mockingbird(self)

#         self._font = self._innertextbox._font
#         self._innertextbox.insert('0.0', content)
#         self._innertextbox.configure(state='disabled')

#     def grid(self, **kwargs):
#         self._innertextbox.grid(row=0, column=0, sticky='ew')
#         return super().grid(**kwargs)

# slightly less laggy

# still laggy tho thanks to configure
class ParagraphDisplayer(ctk.CTkFrame):
    def __init__(self, master: any, content: str):
        super().__init__(master, fg_color='transparent')
        self.master = master
        self.columnconfigure(0, weight=1)

        self._innertextbox = ctk.CTkLabel(
            self,
            text=content,
            bg_color='transparent',
            justify='left',
            wraplength=240
        )
        self._innertextbox.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.bind("<Configure>", 
                  lambda x : self._innertextbox.configure(wraplength=self.winfo_width() - 10))