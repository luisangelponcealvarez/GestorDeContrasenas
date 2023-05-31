import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import csv
import string
import random

class RegistroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Contraseñas")
        
        # Variables para los campos de entrada
        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        
        self.fila_seleccionada = None
        
        # Crear los widgets
        self.crear_widgets()
    
    def crear_widgets(self):
        # Etiquetas
        nombre_label = tk.Label(self, text="Nombre:")
        nombre_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        correo_label = tk.Label(self, text="Correo:")
        correo_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        contrasena_label = tk.Label(self, text="Contraseña:")
        contrasena_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        
        # Campos de entrada
        nombre_entry = tk.Entry(self, textvariable=self.nombre_var)
        nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        correo_entry = tk.Entry(self, textvariable=self.correo_var)
        correo_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        contrasena_entry = tk.Entry(self, textvariable=self.contrasena_var, show="*")
        contrasena_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Botones
        guardar_button = tk.Button(self, text="Guardar", command=self.guardar_datos)
        guardar_button.grid(row=3, column=1, padx=10, pady=5)
        generar_button = tk.Button(self, text="Generar Contraseña", command=self.generar_contrasena)
        generar_button.grid(row=2, column=2, padx=10, pady=5)
        
        # Tabla
        self.tabla = ttk.Treeview(self, columns=("Nombre", "Correo", "Contraseña"), show="headings")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Contraseña", text="Contraseña")
        self.tabla.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        # Agregar scrollbars a la tabla
        scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        scrollbar_y.grid(row=4, column=2, sticky="ns")
        scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.tabla.xview)
        scrollbar_x.grid(row=5, column=0, columnspan=2, sticky="ew")
        
        self.tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Asociar evento de selección de fila a la función de mostrar selección
        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_seleccion)
        
        # Botón Ver Todos
        ver_todos_button = tk.Button(self, text="Ver Todos", command=self.abrir_ventana_todos)
        ver_todos_button.grid(row=5, column=1, padx=10, pady=5)
        
        # Cargar los datos existentes
        self.cargar_datos()
    
    def guardar_datos(self):
        nombre = self.nombre_var.get()
        correo = self.correo_var.get()
        contrasena = self.contrasena_var.get()
        
        if nombre and correo and contrasena:
            datos = [nombre, correo, contrasena]
            
            # Guardar los datos en un archivo CSV
            with open("password.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(datos)
            
            # Limpiar los campos de entrada
            self.nombre_var.set("")
            self.correo_var.set("")
            self.contrasena_var.set("")
            
            # Actualizar la tabla con los nuevos datos
            self.tabla.insert("", "end", values=datos)
            
            messagebox.showinfo("Éxito", "Los datos han sido guardados correctamente.")
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
    
    def cargar_datos(self):
        try:
            with open("password.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        self.tabla.insert("", "end", values=row)
        except FileNotFoundError:
            pass
    
    def mostrar_seleccion(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            datos = self.tabla.item(seleccion[0])['values']
            self.nombre_var.set(datos[0])
            self.correo_var.set(datos[1])
            self.contrasena_var.set(datos[2])
            self.fila_seleccionada = seleccion[0]
    
    def abrir_ventana_todos(self):
        ventana_todos = tk.Toplevel(self)
        ventana_todos.title("Todos los Datos")
        
        # Tabla de "Ver Todos"
        tabla_todos = ttk.Treeview(ventana_todos, columns=("Nombre", "Correo", "Contraseña"), show="headings")
        tabla_todos.heading("Nombre", text="Nombre")
        tabla_todos.heading("Correo", text="Correo")
        tabla_todos.heading("Contraseña", text="Contraseña")
        tabla_todos.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Agregar scrollbars a la tabla
        scrollbar_y = ttk.Scrollbar(ventana_todos, orient="vertical", command=tabla_todos.yview)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(ventana_todos, orient="horizontal", command=tabla_todos.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        
        tabla_todos.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Cargar todos los datos en la tabla
        try:
            with open("password.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        tabla_todos.insert("", "end", values=row)
        except FileNotFoundError:
            pass
        
        # Agregar campos de entrada para copiar los datos
        campos_copia = scrolledtext.ScrolledText(ventana_todos, width=30, height=10)
        campos_copia.pack(side="right", padx=10, pady=10)
        
        # Función para copiar los datos en los campos de entrada
        def copiar_datos():
            seleccion = tabla_todos.focus()
            if seleccion:
                datos = tabla_todos.item(seleccion)['values']
                campos_copia.delete("1.0", "end")
                campos_copia.insert("1.0", f"Nombre: {datos[0]}\nCorreo: {datos[1]}\nContraseña: {datos[2]}")
        
        # Botón para copiar los datos seleccionados
        copiar_button = tk.Button(ventana_todos, text="Copiar Datos", command=copiar_datos)
        copiar_button.pack(pady=5)
        
    def generar_contrasena(self):
        longitud = 12
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
        self.contrasena_var.set(contrasena)


if __name__ == "__main__":
    app = RegistroApp()
    app.mainloop()
