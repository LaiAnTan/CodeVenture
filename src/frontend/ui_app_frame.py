import customtkinter as ctk
from .ui_app import App
from abc import abstractmethod, ABC


class App_Frame(ctk.CTkFrame, ABC):
    """
    Abstract Base Class to use in conjuction with App() for App's
    functionality to work

    Use App_Frame to implement all core windows

    All App_Frames are expected to be
    - ctk.CTkFrame
    - attached DIRECTLY to main_frame
    - the root of the window
    - all widgets can be destroyed and rebuild when refresh is called
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(App().main_frame, fg_color='transparent', *args,
                         **kwargs)

    @abstractmethod
    def attach_elements():
        """
        Attach elements onto the frame
        """
        pass

    @abstractmethod
    def refresh_variables(self):
        """
        Refreshes all variables by resetting them to default values

        Used in conjection with refresh
        """
        pass

    def refresh(self):
        """
        Refresh is in charge of 'refreshing' the page, updating the
        contents with updated values by refreshing all variables
        and reattaching all elements
        """
        self.refresh_variables()
        self.remove_all_widget()
        self.attach_elements()

    def remove_all_widget(self):
        """
        Removes all widget from self

        used in conjunction with refresh
        """
        for widgets in self.winfo_children():
            widgets.destroy()
