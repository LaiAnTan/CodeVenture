import customtkinter as ctk
from customtkinter.windows.widgets.font import CTkFont

lazy_count = 0

class RecommendedAcFrame(ctk.CTkScrollableFrame):
    def __init__(self,
                 master: any,
                 width: int = 200,
                 height: int = 200,
                 corner_radius = None,
                 border_width = None,

                 bg_color = "transparent",
                 fg_color = None,
                 border_color = None,
                 scrollbar_fg_color = None,
                 scrollbar_button_color = None,
                 scrollbar_button_hover_color = None,
                 label_fg_color = None,
                 label_text_color = None,

                 label_text: str = "",
                 label_font = None,
                 label_anchor: str = "center",
                 orientation = "horizontal"):
            super().__init__(master, width,
                             height, corner_radius,
                             border_width, bg_color,
                             fg_color, border_color,
                             scrollbar_fg_color,
                             scrollbar_button_color,
                             scrollbar_button_hover_color,
                             label_fg_color, label_text_color,
                             label_text, label_font,
                             label_anchor, orientation)
            self._scrollbar.grid_forget()
            self.current_showing = 0

            self.bind('<Enter>', self._bound_to_mousewheel)
            self.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        # with Windows OS
        self.bind_all("<MouseWheel>", self.mouse_wheel)

        # with Linux OS
        self.bind_all("<Button-4>", self.mouse_wheel)
        self.bind_all("<Button-5>", self.mouse_wheel)

    def _unbound_to_mousewheel(self, event):
        # with Windows OS
        self.unbind_all("<MouseWheel>")

        # with Linux OS
        self.unbind_all("<Button-4>")
        self.unbind_all("<Button-5>")

    def mouse_wheel(self, event):
        child_num = len(self.winfo_children())

        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            # down scrolled
            if self.current_showing > 0: 
                self.current_showing -= 1
            self._parent_canvas.xview_moveto(self.current_showing / child_num)
            # self._parent_canvas.xview_scroll(1, "units")

        if event.num == 4 or event.delta == 120:
            # up scrolled
            if self.current_showing < child_num: 
                self.current_showing += 1
            self._parent_canvas.xview_moveto(self.current_showing / child_num)
            # self._parent_canvas.xview_scroll(-1, "units")

    def _scroll(self, event):
         print(event)

def add_test_elem(attach_to):
    from .ui_more_info_tile import MoreInfoTile

    global lazy_count

    test = MoreInfoTile(
         60,
         175,
         attach_to
    )
    test.grid(row=0, column=lazy_count, padx=10, pady=10, sticky='ns')

    lazy_count += 1

if __name__ == "__main__":
    from ..ui_app import App
    App()

    test_tile = RecommendedAcFrame(
         master=App().main_frame,
         width=460
    )
    test_tile.grid(row=0, column=0)

    add_button = ctk.CTkButton(
         master=App().main_frame,
         text='Add Test Elem',
         command=lambda : add_test_elem(test_tile)
    )
    add_button.grid(row=1, column=0, padx=5, pady=5)

    App().main_frame.grid(row=0, column=0)
    App().mainloop()