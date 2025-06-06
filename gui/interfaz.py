import tkinter as tk
from tkinter import *
from tkinter import messagebox
from afn.afn_Asignacion import validar_asignacion, simular_automata
from afn.afn_if import validar_if_con_bloques_anidados, debug_tokenizacion  # Importar las funciones del AFN IF
from core.octave_lexer import lexer
from core.octave_parser import parser, limpiar_mensajes, obtener_mensajes 
from core.analisis_semantico import analisis_semantico, obtener, limpiar

class InterfazAsignacion:
    def __init__(self, master):
        self.master = master
        self.master.title("COMPILADOR")
        self.master.geometry("900x500")
        self.master.resizable(True, True)
        
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.main_frame.grid_columnconfigure(0, weight=1)  # Entrada
        self.main_frame.grid_columnconfigure(1, weight=0)  # Botones  
        self.main_frame.grid_columnconfigure(2, weight=2)  # Resultado
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        self.crear_seccion_entrada()
        self.crear_seccion_botones()
        self.crear_seccion_resultado()
    
    def crear_seccion_entrada(self):
        self.frame_entrada = tk.Frame(self.main_frame, relief="ridge", bd=2)
        self.frame_entrada.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self.label_titulo_entrada = tk.Label(self.frame_entrada, text="ENTRADA", 
                                           font=("Arial", 12, "bold"))
        self.label_titulo_entrada.pack(pady=10)
        
        self.label_instruccion = tk.Label(self.frame_entrada, 
                                        text="Ingrese una sentencia:")
        self.label_instruccion.pack(pady=10)
        
        self.entrada_text_frame = tk.Frame(self.frame_entrada)
        self.entrada_text_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.entrada_scrollbar = tk.Scrollbar(self.entrada_text_frame)
        self.entrada_scrollbar.pack(side="right", fill="y")
        
        self.entry = tk.Text(self.entrada_text_frame, width=30, height=8, 
                           font=("Arial", 10), wrap="word",
                           yscrollcommand=self.entrada_scrollbar.set)
        self.entry.pack(side="left", fill="both", expand=True)
        
        self.entrada_scrollbar.config(command=self.entry.yview)
        
        self.label_espacio = tk.Label(self.frame_entrada, text="")
        self.label_espacio.pack(expand=True)
    
    def crear_seccion_botones(self):
        self.frame_botones = tk.Frame(self.main_frame, relief="ridge", bd=2)  
        self.frame_botones.grid(row=0, column=1, sticky="nsew", padx=5)
        self.frame_botones.grid_propagate(False)  
        
        self.label_titulo_botones = tk.Label(self.frame_botones, text="TIPO", 
                                           font=("Arial", 12, "bold"))
        self.label_titulo_botones.pack(pady=10)
        
        self.container_botones = tk.Frame(self.frame_botones)
        self.container_botones.pack(expand=True)
        
        # Botón ValidarAsignacion
        self.btn_validar_asig = tk.Button(self.container_botones, text="Asigacion", 
                                   command=self.validar_asignacion,
                                   width=12, height=2,
                                   bg="#4CAF50", fg="white",
                                   font=("Arial", 10, "bold"))
        self.btn_validar_asig.pack(pady=5)
        
        # Botón ValidarFor
        self.btn_validar_for = tk.Button(self.container_botones, text="For", 
                                   command=lambda: self.validaciones("For"),
                                   width=12, height=2,
                                   bg="#4CAF50", fg="white",
                                   font=("Arial", 10, "bold"))
        self.btn_validar_for.pack(pady=5)
        
        # Botón ValidarWhile
        self.btn_validar_while = tk.Button(self.container_botones, text="While", 
                                   command=lambda: self.validaciones("While"),
                                   width=12, height=2,
                                   bg="#4CAF50", fg="white",
                                   font=("Arial", 10, "bold"))
        self.btn_validar_while.pack(pady=5)
        
        # Botón ValidarIf - NUEVO
        self.btn_validar_if = tk.Button(self.container_botones, text="If", 
                                   command=self.validar_if,
                                   width=12, height=2,
                                   bg="#2196F3", fg="white",
                                   font=("Arial", 10, "bold"))
        self.btn_validar_if.pack(pady=5)
        
        # Botón Limpiar
        self.btn_limpiar = tk.Button(self.container_botones, text="Limpiar", 
                                   command=self.limpiar_campos,
                                   width=12, height=2,
                                   bg="#FF9800", fg="white",
                                   font=("Arial", 10, "bold"))
        self.btn_limpiar.pack(pady=5)
        
        # Botón Salir
        self.btn_salir = tk.Button(self.container_botones, text="Salir", 
                                 command=self.salir,
                                 width=12, height=2,
                                 bg="#F44336", fg="white",
                                 font=("Arial", 10, "bold"))
        self.btn_salir.pack(pady=5)
    
    def crear_seccion_resultado(self):
        self.frame_resultado = tk.Frame(self.main_frame, relief="ridge", bd=2)
        self.frame_resultado.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        self.label_titulo_resultado = tk.Label(self.frame_resultado, text="RESULTADO", 
                                             font=("Arial", 12, "bold"))
        self.label_titulo_resultado.pack(pady=10)
        
        self.text_frame = tk.Frame(self.frame_resultado)
        self.text_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side="right", fill="y")
        
        self.text_box = tk.Text(self.text_frame, wrap="word", 
                              yscrollcommand=self.scrollbar.set,
                              font=("Courier", 10),
                              bg="#f5f5f5")
        self.text_box.pack(side="left", fill="both", expand=True)
        
        self.scrollbar.config(command=self.text_box.yview)
        
        self.text_box.insert(tk.END, "Ingrese una sentencia y seleccione el tipo para ver el resultado.\n\n")
        self.text_box.config(state="disabled") 
    
    def validar_asignacion(self):
        cadena = self.entry.get("1.0", tk.END).strip()
        
        if not cadena:
            messagebox.showwarning("Advertencia", "Por favor ingrese una asignación")
            return
        
        try:
            self.text_box.config(state="normal")
            
            self.text_box.delete("1.0", tk.END)
            
            self.text_box.insert(tk.END, f"Validando:\n{cadena}\n")
            self.text_box.insert(tk.END, "="*50 + "\n\n")
            
            resultado = simular_automata(cadena)
            self.text_box.insert(tk.END, resultado)
            
            es_valida = validar_asignacion(cadena)
            
            self.text_box.insert(tk.END, "\n" + "="*50 + "\n")
            
            if es_valida:
                self.text_box.insert(tk.END, "✓ ASIGNACIÓN VÁLIDA", "valida")
                self.text_box.tag_config("valida", foreground="green", font=("Arial", 12, "bold"))
                
            else:
                self.text_box.insert(tk.END, "✗ ASIGNACIÓN INVÁLIDA", "invalida")
                self.text_box.tag_config("invalida", foreground="red", font=("Arial", 12, "bold"))
                
            
            self.text_box.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar la asignación: {str(e)}")
            self.text_box.config(state="disabled")
    
    def validar_if(self):
        """Nueva función para validar estructuras IF"""
        cadena = self.entry.get("1.0", tk.END).strip()
        
        if not cadena:
            messagebox.showwarning("Advertencia", "Por favor ingrese una estructura if")
            return
        
        # Verificar que contenga un 'if'
        hay_if = any("if" in palabra.lower() for palabra in cadena.split())
        
        if not hay_if:
            messagebox.showwarning("Advertencia", "La sentencia debe contener un 'if'")
            return
        
        try:
            self.text_box.config(state="normal")
            self.text_box.delete("1.0", tk.END)
            
            self.text_box.insert(tk.END, f"Validando estructura IF:\n{cadena}\n")
            self.text_box.insert(tk.END, "="*60 + "\n\n")
            
            # Capturar la salida de la función de validación
            import io
            import sys
            from contextlib import redirect_stdout
            
            # Crear un buffer para capturar la salida
            salida_buffer = io.StringIO()
            
            # Redirigir stdout temporalmente
            with redirect_stdout(salida_buffer):
                es_valida = validar_if_con_bloques_anidados(cadena)
            
            # Obtener la salida capturada
            salida_capturada = salida_buffer.getvalue()
            
            # Mostrar el análisis detallado
            self.text_box.insert(tk.END, salida_capturada)
            
            # Mostrar el resultado final
            self.text_box.insert(tk.END, "\n" + "="*60 + "\n")
            
            if es_valida:
                self.text_box.insert(tk.END, "✓ ESTRUCTURA IF VÁLIDA", "valida")
                self.text_box.tag_config("valida", foreground="green", font=("Arial", 12, "bold"))
            else:
                self.text_box.insert(tk.END, "✗ ESTRUCTURA IF INVÁLIDA", "invalida")
                self.text_box.tag_config("invalida", foreground="red", font=("Arial", 12, "bold"))
            
            self.text_box.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar la estructura if: {str(e)}")
            self.text_box.config(state="disabled")
    
    def validaciones(self, tipo):
        cadena = self.entry.get("1.0", tk.END).strip()
        
        if not cadena:
            messagebox.showwarning("Advertencia", "Por favor ingrese una sentencia")
            return
        if tipo == "For":
            hay_for = any("for" in pal for pal in cadena.split())
            
            if not hay_for:
                messagebox.showwarning("Advertencia", "La sentencia debe contener un 'for'")
                return
            
        elif tipo == "While":
            hay_while = any("while" in pal for pal in cadena.split())
            
            if not hay_while:
                messagebox.showwarning("Advertencia", "La sentencia debe contener un 'while'")
                return
        
        try:
            self.text_box.config(state="normal")
            
            self.text_box.delete("1.0", tk.END)
            
            self.text_box.insert(tk.END, f"Validando:\n{cadena}\n")
            self.text_box.insert(tk.END, "="*50 + "\n")
            
            self.text_box.insert(tk.END, "=== ANÁLISIS LÉXICO ===\n")
            lexer.input(cadena)
            for tok in lexer:
                self.text_box.insert(tk.END, f"{tok.type}: {tok.value}\n")
            
            self.text_box.insert(tk.END, "\n=== ANÁLISIS SINTÁCTICO ===\n")
            limpiar_mensajes()
            resultado = parser.parse(cadena)
            mensajes = obtener_mensajes()  
            if mensajes:
                for mensaje in mensajes:
                    self.text_box.insert(tk.END, f"{mensaje}\n")
            
            error = any("Error" in mensaje for mensaje in mensajes)
            mensajes_sm = [] 
            if not error:
                if resultado:
                    self.text_box.insert(tk.END, f"\n[SINTAXIS] Árbol sintáctico: {resultado}")
                self.text_box.insert(tk.END, "\n\n=== ANÁLISIS SEMÁNTICO ===\n")
                limpiar()
                analisis_semantico(resultado)
                mensajes_sm = obtener()  
                if mensajes_sm:
                    for mensaje in mensajes_sm:
                        self.text_box.insert(tk.END, f"{mensaje}\n")
                
                self.text_box.insert(tk.END, "\n" + "="*50 + "\n")
            else:
                self.text_box.insert(tk.END, "\n\n=== ANÁLISIS SEMÁNTICO ===\n")
                self.text_box.insert(tk.END, "[SEMÁNTICA] Error: análisis semántico interrumpido por errores sintácticos.")
                mensajes_sm.append("[SEMÁNTICA] Error: análisis semántico interrumpido por errores sintácticos.")
                self.text_box.insert(tk.END, "\n" + "="*50 + "\n")
            
            hay_error = any("Error:" in mensaje for mensaje in mensajes_sm)
            
            if not hay_error and not error:
                self.text_box.insert(tk.END, "✓ SENTENCIA VÁLIDA", "valida")
                self.text_box.tag_config("valida", foreground="green", font=("Arial", 12, "bold"))
            else:
                self.text_box.insert(tk.END, "✗ SENTENCIA INVÁLIDA", "invalida")
                self.text_box.tag_config("invalida", foreground="red", font=("Arial", 12, "bold"))
            
            self.text_box.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar la sentencia: {str(e)}")
            self.text_box.config(state="disabled")
            
    def limpiar_campos(self):
        self.entry.delete("1.0", tk.END)
        
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, "Ingrese una sentencia y seleccione el tipo para ver el resultado.\n\n")
        self.text_box.config(state="disabled")
        self.entry.focus()
    
    def salir(self):
        if messagebox.askquestion("Salir", "¿Está seguro que desea salir?") == "yes":
            self.master.quit()

# Para ejecutar la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazAsignacion(root)
    root.mainloop()