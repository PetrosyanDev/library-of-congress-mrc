from tkinter import messagebox
import sys
import ui
from helpers import *

def main():
    try:
        app = ui.App()
        app.mainloop()
    except Exception as e:
        messagebox.showwarning("Warning", f"Unexpected Error: {e}") 
        sys.exit()

if __name__ == "__main__":
    main()
