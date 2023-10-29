from typing import Tuple
import customtkinter as ctk
from tkinter import Event
from customtkinter.windows.widgets.font import CTkFont


class TextBox_Placeholder(ctk.CTkTextbox):

    """
    Custom made tkinter widget that inherits from ctkTextbox.

    Purpose: to have placeholder text.
    """
    def __init__(self, master: any, width: int = 200, height: int = 200,
                 corner_radius: int | None = None,
                 border_width: int | None = None,
                 border_spacing: int = 3,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None,
                 text_color: str | None = None,
                 scrollbar_button_color: str | Tuple[str, str] | None = None,
                 scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
                 font: tuple | CTkFont | None = None,
                 activate_scrollbars: bool = True,
                 placeholder: str = 'Default Placeholder',
                 placeholder_color: str = 'grey',
                 **kwargs):
        """
        Initialises the class.
        """
        super().__init__(master, width, height, corner_radius,
                         border_width, border_spacing, bg_color,
                         fg_color, border_color, text_color,
                         scrollbar_button_color, scrollbar_button_hover_color,
                         font, activate_scrollbars, **kwargs)

        self.placeholder = placeholder
        self.placeholder_clr = placeholder_color

        self.default_clr = self._text_color

        if self.placeholder_clr == self.default_clr:
            raise ValueError("Placeholder color is the same as Default Input \
color!")

        self.bind("<Key>", self.placeholder_handler)
        self.bind("<FocusIn>", self.focus_in)
        self.insert_placeholder()

    def next_is_empty(self):
        value = self.get("0.0", ctk.END)
        if len(value) == 0:
            return True
        if len(value) <= 2 and value[-1] == '\n':
            return True
        return False

    def placeholder_handler(self, details: Event):
        if details.keysym == 'BackSpace':
            if self._text_color != self.placeholder_clr \
                    and self.next_is_empty():
                self.insert_placeholder()
            if self._text_color == self.placeholder_clr:
                self.mark_set("insert", "0.0")
                return "break"
        elif self._text_color != self.default_clr:
            self.configure(text_color=self.default_clr)
            self.delete("0.0", ctk.END)

    def insert_placeholder(self):
        self.configure(text_color=self.placeholder_clr)
        self.delete("0.0", ctk.END)
        super().insert("0.0", self.placeholder)

    def focus_in(self, details: Event | None = None):
        if self._text_color == self.placeholder_clr:
            self.mark_set("insert", "0.0")
            return "break"

    def insert(self, index, text, tags=None):
        if self._text_color == self.placeholder_clr:
            self.configure(text_color=self.default_clr)
            self.delete("0.0", ctk.END)
        return super().insert(index, text, tags)

    def get(self, index1, index2=None):
        if self._text_color == self.placeholder_clr:
            return "\n"
        return super().get(index1, index2)


if __name__ == "__main__":
    from ...ui_app import App
    a = App()

    test = TextBox_Placeholder(a.main_frame)
    test.grid(row=0, column=0, padx=5, pady=5)

    nothing = ctk.CTkButton(a.main_frame, text='Out of focus',
                            command=lambda: nothing.focus())
    nothing.grid(row=1, column=0, padx=5, pady=5)

    a.main_frame.grid(row=0, column=0)
    a.mainloop()
