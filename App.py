import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import random
import string

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inicio de Sesión")

        self.usuario_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()

        usuario_label = tk.Label(self, text="Usuario:")
        
        usuario_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        usuario_entry = tk.Entry(self, textvariable=self.usuario_var)
        usuario_entry.grid(row=0, column=1, columnspan=2, sticky="we", padx=10, pady=5)

        contrasena_label = tk.Label(self, text="Contraseña:")
        contrasena_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        contrasena_entry = tk.Entry(self, textvariable=self.contrasena_var, show="*")
        contrasena_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=10, pady=5)

        iniciar_sesion_button = tk.Button(self, text="Iniciar Sesión", command=self.iniciar_sesion)
        iniciar_sesion_button.grid(row=2, column=1, pady=10)

    def iniciar_sesion(self):
        usuario = self.usuario_var.get()
        contrasena = self.contrasena_var.get()

        if usuario == "admin" and contrasena == "admin":
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
            self.destroy()
            app = RegistroApp()
            app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

class RegistroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro de Usuarios")

        # Crear variables para almacenar los datos ingresados y la fila seleccionada
        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.fila_seleccionada = None

        # Crear la tabla para mostrar los datos
        self.tabla = ttk.Treeview(self, columns=("Nombre", "Correo", "Contraseña"), show="headings", selectmode='browse')
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Contraseña", text="Contraseña")
        self.tabla.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        self.tabla.bind('<<TreeviewSelect>>', self.mostrar_seleccion)

        # Crear etiquetas y campos de entrada
        nombre_label = tk.Label(self, text="Nombre:")
        nombre_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        nombre_entry = tk.Entry(self, textvariable=self.nombre_var)
        nombre_entry.grid(row=1, column=1, columnspan=4, sticky="we", padx=10, pady=5)

        correo_label = tk.Label(self, text="Correo:")
        correo_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        correo_entry = tk.Entry(self, textvariable=self.correo_var)
        correo_entry.grid(row=2, column=1, columnspan=4, sticky="we", padx=10, pady=5)

        contrasena_label = tk.Label(self, text="Contraseña:")
        contrasena_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.contrasena_entry = tk.Entry(self, textvariable=self.contrasena_var, show="*")
        self.contrasena_entry.grid(row=3, column=1, columnspan=3, sticky="we", padx=10, pady=5)

        # Resto del código...

class RegistroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro de Usuarios")

        # Crear variables para almacenar los datos ingresados y la fila seleccionada
        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.fila_seleccionada = None
        
        # Crear la tabla para mostrar los datos
        self.tabla = ttk.Treeview(self, columns=("Nombre", "Correo", "Contraseña"), show="headings", selectmode='browse')
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Contraseña", text="Contraseña")
        self.tabla.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        self.tabla.bind('<<TreeviewSelect>>', self.mostrar_seleccion)
        
        # Crear etiquetas y campos de entrada
        nombre_label = tk.Label(self, text="Nombre:")
        nombre_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        nombre_entry = tk.Entry(self, textvariable=self.nombre_var)
        nombre_entry.grid(row=1, column=1, columnspan=4, sticky="we", padx=10, pady=5)
        
        correo_label = tk.Label(self, text="Correo:")
        correo_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        correo_entry = tk.Entry(self, textvariable=self.correo_var)
        correo_entry.grid(row=2, column=1, columnspan=4, sticky="we", padx=10, pady=5)
        
        contrasena_label = tk.Label(self, text="Contraseña:")
        contrasena_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.contrasena_entry = tk.Entry(self, textvariable=self.contrasena_var, show="*")
        self.contrasena_entry.grid(row=3, column=1, columnspan=3, sticky="we", padx=10, pady=5)
        
        # Botón para generar contraseña aleatoria
        generar_button = tk.Button(self, text="Generar Contraseña", command=self.generar_contrasena)
        generar_button.grid(row=3, column=4, padx=10, pady=5)
        
        # Botón para guardar los datos
        guardar_button = tk.Button(self, text="Guardar", command=self.guardar_datos)
        guardar_button.grid(row=4, column=0, pady=10)
        
        # Crear campo de búsqueda y botón de búsqueda
        buscar_label = tk.Label(self, text="Buscar:")
        buscar_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.buscar_entry = tk.Entry(self)
        self.buscar_entry.grid(row=5, column=1, sticky="we", padx=10, pady=5)
        buscar_button = tk.Button(self, text="Buscar", command=self.buscar_datos)
        buscar_button.grid(row=5, column=2, padx=10, pady=5)
        
        # Botón para ver todos los datos
        ver_todos_button = tk.Button(self, text="Ver Todos", command=self.ver_todos_los_datos)
        ver_todos_button.grid(row=5, column=3, padx=10, pady=5)
        
        # Cargar los datos desde el archivo CSV
        self.cargar_datos()
    
    def cargar_datos(self):
        try:
            with open("password.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        self.tabla.insert("", "end", values=row)
        except FileNotFoundError:
            pass
    
    def guardar_datos(self):
        nombre = self.nombre_var.get()
        correo = self.correo_var.get()
        contrasena = self.contrasena_var.get()
        
        if nombre and correo and contrasena:
            if self.fila_seleccionada:
                # Editar los datos de la fila seleccionada
                self.tabla.item(self.fila_seleccionada, values=(nombre, correo, contrasena))
                self.fila_seleccionada = None
                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
            else:
                # Agregar los datos a la tabla
                self.tabla.insert("", "end", values=(nombre, correo, contrasena))
                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Datos guardados correctamente.")
            
            # Guardar los datos en un archivo CSV
            with open("password.csv", "w", newline="") as file:
                writer = csv.writer(file)
                for item in self.tabla.get_children():
                    row = self.tabla.item(item)["values"]
                    writer.writerow(row)
        else:
            messagebox.showerror("Error", "Por favor, rellene todos los campos.")
    
    def mostrar_seleccion(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            self.fila_seleccionada = seleccion
            datos = self.tabla.item(seleccion)['values']
            self.nombre_var.set(datos[0])
            self.correo_var.set(datos[1])
            self.contrasena_var.set(datos[2])
            
            # Mostrar la contraseña en el campo de entrada
            self.contrasena_entry.config(show="")
    
    def limpiar_campos(self):
        self.nombre_var.set("")
        self.correo_var.set("")
        self.contrasena_var.set("")
        
        # Ocultar la contraseña en el campo de entrada
        self.contrasena_entry.config(show="*")
    
    def buscar_datos(self):
        termino = self.buscar_entry.get()
        if termino:
            # Eliminar todas las filas de la tabla
            self.tabla.delete(*self.tabla.get_children())
            
            # Cargar los datos desde el archivo CSV y filtrar las filas que coincidan con el término de búsqueda
            try:
                with open("password.csv", "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) == 3 and any(termino.lower() in value.lower() for value in row):
                            self.tabla.insert("", "end", values=row)
            except FileNotFoundError:
                pass
        else:
            # Si el campo de búsqueda está vacío, mostrar todos los datos nuevamente
            self.ver_todos_los_datos()
    
    def ver_todos_los_datos(self):
        # Eliminar todas las filas de la tabla
        self.tabla.delete(*self.tabla.get_children())
        
        # Cargar los datos desde el archivo CSV
        self.cargar_datos()
    
    def generar_contrasena(self):
        longitud = 20
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contrasena_generada = ''.join(random.choice(caracteres) for _ in range(longitud))
        self.contrasena_var.set(contrasena_generada)
    
    def eliminar_dato(self):
        if self.fila_seleccionada:
            confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar los datos seleccionados?")
            if confirmacion:
                self.tabla.delete(self.fila_seleccionada)
                self.fila_seleccionada = None
                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Datos eliminados correctamente.")
                
                # Guardar los datos actualizados en el archivo CSV
                with open("password.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    for item in self.tabla.get_children():
                        row = self.tabla.item(item)["values"]
                        writer.writerow(row)
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una fila para eliminar.")

if __name__ == "__main__":
    login_app = LoginApp()
    login_app.mainloop()
    app = RegistroApp()
    app.mainloop()
