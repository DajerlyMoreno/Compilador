import tkinter as tk
from gui.interfaz import inicio  # Importamos la clase

if __name__ == "__main__":
    root = tk.Tk()
    app = inicio(root)
    root.mainloop()
