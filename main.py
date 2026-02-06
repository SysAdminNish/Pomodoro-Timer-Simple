
import tkinter as tk

from model import Model
from view import View
from presenter import Presenter


def main():
	root = tk.Tk()
	# Increase default scaling on Windows for crisp large UI when necessary
	try:
		if root.tk.call("tk", "windowingsystem") == "win32":
			root.call("tk", "scaling", 1.25)
	except Exception:
		pass
	root.configure(bg=View.BG)
	model = Model()
	view = View(root, width=520, height=760)
	Presenter(model, view, root)
	root.mainloop()


if __name__ == "__main__":
	main()



