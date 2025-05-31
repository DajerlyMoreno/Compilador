import tkinter as tk
from gui.interfaz import InterfazAsignacion  # Importamos la clase

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazAsignacion(root)
    root.mainloop()
