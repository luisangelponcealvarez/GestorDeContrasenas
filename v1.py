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

if __name__ == "__main__":
    login_app = LoginApp()
    login_app.mainloop()
