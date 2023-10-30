from __future__ import annotations
import customtkinter as ctk
from customtkinter.windows.widgets.font import CTkFont


class RefreshableScrollableFrame(ctk.CTkScrollableFrame):

    """
    A refreshable frame

    "Refreshable" as in, you can remove (or add) widget
    anywhere you want, and it will refresh and redisplay
    all contents without (hopefully) errors

    Its also scrollable, which means you can set
    where is it scroll to after you add // remove a widget
    """

    def __init__(self,
                 master: any,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: int | str | None = None,
                 border_width: int | str | None = None,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = None,
                 border_color: str | tuple[str, str] | None = None,
                 scrollbar_fg_color: str | tuple[str, str] | None = None,
                 scrollbar_button_color: str | tuple[str, str] | None = None,
                 scrollbar_button_hover_color: str | tuple[str, str] | None = None,
                 label_fg_color: str | tuple[str, str] | None = None,
                 label_text_color: str | tuple[str, str] | None = None,
                 label_text: str = "", label_font: tuple | CTkFont | None = None,
                 label_anchor: str = "center",
                 orientation="vertical"
                 ):
        """
        Initialises the class.
        """

        super().__init__(master, width, height, corner_radius,
                         border_width, bg_color, fg_color, border_color,
                         scrollbar_fg_color, scrollbar_button_color,
                         scrollbar_button_hover_color, label_fg_color,
                         label_text_color, label_text, label_font,
                         label_anchor, orientation)
        self.columnconfigure(0, weight=1)
        self.tracking: list[RSFWidget] = []

    def add_element_specific(self, index, frame) -> None:
        self.tracking.insert(index, frame)

    def get_tracking_no(self) -> int:
        return len(self.tracking)

    def track_element(self, frame) -> None:
        self.tracking.append(frame)

    def get_tracking_list(self) -> list[RSFWidget]:
        return self.tracking

    def get_subframe(self, index) -> None | RSFWidget:
        try:
            return self.tracking[index]
        except IndexError:
            return None

    def refresh_elements(self) -> None:
        """
        Remove all frame in this frame
        Then, reattach them onto the frame

        Use when there are changes in the ordering of self.content_frames
        (removal or addition)
        """

        for children in self.winfo_children():
            children.grid_forget()

        for index, components in enumerate(self.tracking):
            self.rowconfigure(index, weight=1)
            components.grid(row=index, column=0, padx=5, pady=(0, 10),
                            sticky='ew')

    def remove_element(self, to_remove: RSFWidget) -> None:
        self.tracking.remove(to_remove)

    def swap_order(self, index1, index2) -> None:
        """
        Swaps order of 2 widgets, thats all it does
        """

        self.tracking[index1], self.tracking[index2] = \
            self.tracking[index2], self.tracking[index1]
        self.refresh_elements()

    def scroll_frame(self, how_much: float) -> None:
        """
        Adjusts the view in the window so that FRACTION of the
        total height of the canvas is off-screen to the top.
        """
        self.update_idletasks()
        self._parent_canvas.yview_moveto(str(how_much))


class RSFWidget(ctk.CTkFrame):

    """
    Widget to use together with refreshable scrollable frame

    allows you to remove the widget no matter where it is
    with (hopefully), no cursed grid operation
    """

    def __init__(self,
                 master: RefreshableScrollableFrame,
                 width: int = 200,
                 height: int = 200,
                 corner_radius=None,
                 border_width=None,
                 bg_color="transparent",
                 fg_color=None,
                 border_color=None,
                 background_corner_colors=None,
                 overwrite_preferred_drawing_method=None,
                 **kwargs):
        super().__init__(master, width, height,
                         corner_radius, border_width,
                         bg_color, fg_color, border_color,
                         background_corner_colors,
                         overwrite_preferred_drawing_method,
                         **kwargs)
        self.parent_frame = master
        self.focus_widget = None

    def set_focus_widget(self, widget) -> None:
        """
        sets the focus widget

        focus widget is the widget that will be focused on
        when its previous instance is removed
        """
        self.focus_widget = widget

    def get_index_instance(self) -> None:
        """
        Returns the index it is in according to it's parent
        """

        for index, x in enumerate(self.parent_frame.get_tracking_list()):
            if x is self:
                return index
        return -1

    def delete_self(self) -> None:
        """
        Remove ownself from parent
        - Sets focus to the next (or previous, if deleted one was the last
            element) Entry Frame
        - Scrolls the content frame to ensure focused entry is in frame
        """

        next_index = self.get_index_instance()
        self.grid_forget()
        self.parent_frame.remove_element(self)

        parent_tracking = self.parent_frame.get_tracking_list()
        if parent_tracking:
            scroll_to = next_index / len(parent_tracking)
            if scroll_to >= 1:
                scroll_to = (next_index - 1) / (len(parent_tracking) + 1)
        else:
            scroll_to = 0

        next_index_widget = self.parent_frame.get_subframe(next_index)
        if next_index_widget is None:
            if parent_tracking:
                parent_tracking[-1].focus()
            else:
                self.parent_frame.focus()

        self.parent_frame.refresh_elements()
        self.parent_frame.scroll_frame(scroll_to)
        self.destroy()

    def focus(self) -> None:
        self.focus_widget.focus()
