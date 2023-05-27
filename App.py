import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import random
import string

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
        self.tabla.pack(pady=10)
        self.tabla.bind('<<TreeviewSelect>>', self.mostrar_seleccion)
        
        # Crear etiquetas y campos de entrada
        nombre_label = tk.Label(self, text="Nombre:")
        nombre_label.pack()
        nombre_entry = tk.Entry(self, textvariable=self.nombre_var)
        nombre_entry.pack()
        
        correo_label = tk.Label(self, text="Correo:")
        correo_label.pack()
        correo_entry = tk.Entry(self, textvariable=self.correo_var)
        correo_entry.pack()
        
        contrasena_label = tk.Label(self, text="Contraseña:")
        contrasena_label.pack()
        self.contrasena_entry = tk.Entry(self, textvariable=self.contrasena_var, show="*")
        self.contrasena_entry.pack()
        
        # Botón para generar una contraseña aleatoria
        generar_button = tk.Button(self, text="Generar Contraseña", command=self.generar_contrasena)
        generar_button.pack(pady=5)
        
        # Botón para guardar los datos
        guardar_button = tk.Button(self, text="Guardar", command=self.guardar_datos)
        guardar_button.pack(pady=10)
        
        # Cargar los datos desde el archivo CSV
        self.cargar_datos()
    
    def cargar_datos(self):
        try:
            with open("passwords.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        self.tabla.insert("", "end", values=row)
        except FileNotFoundError:
            pass
    
    def generar_contrasena(self):
        longitud = 20
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
        self.contrasena_var.set(contrasena)
    
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
            with open("passwords.csv", "w", newline="") as file:
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

if __name__ == "__main__":
    app = RegistroApp()
    app.mainloop()
