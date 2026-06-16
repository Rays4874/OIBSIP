import tkinter as tk
from ui import PasswordGeneratorApp

def main():
    root = tk.Tk()
    # Apply standard Tkinter styling tweaks if desired
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()