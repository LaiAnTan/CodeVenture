from src.frontend.ui_app import App
from src.populate_db import populate_databases
import src.frontend.ui_std_window_gen as wingen
from config import ROOT_DIR

def reset_databases() -> None:
    pass

def main() -> None:
    """
    Main function of the program.

    @return None
    """
    reset_databases()
    populate_databases()
    a = App()
    wingen.loginPage(a)
    a.mainloop()


if __name__ == "__main__":
    main()
