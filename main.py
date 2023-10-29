import sys

from src.frontend.ui_app import App
from src.setup import populate_databases, reset_databases
import src.frontend.ui_std_window_gen as wingen

def main() -> None:
    """
    Main function of the program.

    @return None
    """
    if len(sys.argv) == 2 and sys.argv[1] == "--reset":
        reset_databases()
    populate_databases()
    a = App()
    wingen.loginPage()
    a.mainloop()


if __name__ == "__main__":
    main()
