from App import App
from ui_login import LoginWindow
from populate_db import populate_databases
import ui_window_gen as wingen

def main():
    populate_databases()
    a = App()
    wingen.loginPage(a)
    a.mainloop()

if __name__ == "__main__":
    main()
