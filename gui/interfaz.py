import tkinter as tk

class inicio:
    def __init__(self, master):
        self.master = master
        self.master.title("Interfaz de Usuario")
        self.master.geometry("400x300")

        self.label = tk.Label(master, text="Bienvenido a la Interfaz de Usuario")
        self.label.pack(pady=20)

        self.button = tk.Button(master, text="Salir", command=self.salir)
        self.button.pack(pady=10)

    def salir(self):
        self.master.quit()  # Cierra la ventana principal