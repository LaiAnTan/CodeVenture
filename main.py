from app import App
from window_gen import selection_screen

if __name__ == "__main__":
	test = App()
	selection_screen(test)
	test.mainloop()