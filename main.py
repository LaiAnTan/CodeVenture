from src.frontend.ui_app import App
from src.populate_db import populate_databases
import src.frontend.ui_std_window_gen as wingen


def main() -> None:
    """
    Main function of the program.

    @return None
    """
    populate_databases()
    # initializes Activity Database Dictionary (ADD)
    a = App()
    wingen.loginPage(a)
    a.mainloop()


if __name__ == "__main__":
    main()
