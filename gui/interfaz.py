import tkinter as tk
from tkinter import *
from afn.afn_Asignacion import validar_asignacion, simular_automata
class inicio:
    def __init__(self, master):
        self.master = master
        self.master.title("Interfaz de Usuario")
        self.master.geometry("400x300")

        self.label = tk.Label(master, text="Bienvenido")
        self.label.pack(pady=20)

        self.btnAsignacion = tk.Button(master, text="Asignación", command=self.asignacion)
        self.btnAsignacion.pack(pady=10)
        self.button = tk.Button(master, text="Salir", command=self.salir)
        self.button.pack(pady=10)

    def salir(self):
        self.master.quit()  # Cierra la ventana principal
    
    def asignacion(self):
        self.master.withdraw()  # Oculta la ventana principal
        self.new_window = tk.Toplevel(self.master)
        self.app = Asignacion(self.new_window)

class Asignacion:
    def __init__(self, master):
        self.master = master
        self.master.title("Validación de Asignación")
        self.master.geometry("500x400")

        self.label = tk.Label(master, text="Ingrese una asignación:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(master)
        self.entry.pack(pady=10)

        self.btnValidar = tk.Button(master, text="Validar", command=self.validar_asignacion)
        self.btnValidar.pack(pady=10)

        # Frame para el Text y Scrollbar
        self.text_frame = tk.Frame(master)
        self.text_frame.pack(pady=10, fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.text_box = tk.Text(self.text_frame, wrap="word", yscrollcommand=self.scrollbar.set, height=10)
        self.text_box.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.text_box.yview)

    def validar_asignacion(self):
        cadena = self.entry.get()
        resultado = simular_automata(cadena)

        # Limpiar el contenido anterior del Text
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, resultado)

        if validar_asignacion(cadena):
            tk.messagebox.showinfo("Resultado", "Asignación válida")
        else:
            tk.messagebox.showerror("Resultado", "Asignación inválida")
