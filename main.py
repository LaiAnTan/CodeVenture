from ui.ui_app import App
from populate_db import populate_databases
import ui.ui_std_window_gen as wingen
import customtkinter as ctk


def main() -> None:
    """
    Main function of the program.

    @return None
    """
    populate_databases()
    a = App()
    wingen.loginPage(a)
    a.mainloop()

if __name__ == "__main__":
    main()
