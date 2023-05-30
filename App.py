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

        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()
        self.contrasena_archivo_var = tk.StringVar()
        self.fila_seleccionada = None

        self.tabla = ttk.Treeview(self, columns=("Nombre", "Correo", "Contraseña"), show="headings", selectmode='browse')
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Contraseña", text="Contraseña")
        self.tabla.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        self.tabla.bind('<<TreeviewSelect>>', self.mostrar_seleccion)

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
        contrasena_entry = tk.Entry(self, textvariable=self.contrasena_var, show="*")
        contrasena_entry.grid(row=3, column=1, columnspan=4, sticky="we", padx=10, pady=5)

        agregar_button = tk.Button(self, text="Agregar", command=self.agregar_usuario)
        agregar_button.grid(row=4, column=0, padx=10, pady=10)

        actualizar_button = tk.Button(self, text="Actualizar", command=self.actualizar_usuario)
        actualizar_button.grid(row=4, column=1, padx=10, pady=10)

        eliminar_button = tk.Button(self, text="Eliminar", command=self.eliminar_usuario)
        eliminar_button.grid(row=4, column=2, padx=10, pady=10)

        contrasena_archivo_label = tk.Label(self, text="Contraseña para el archivo:")
        contrasena_archivo_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        contrasena_archivo_entry = tk.Entry(self, textvariable=self.contrasena_archivo_var, show="*")
        contrasena_archivo_entry.grid(row=5, column=1, columnspan=4, sticky="we", padx=10, pady=5)

        establecer_contrasena_button = tk.Button(self, text="Establecer contraseña en el archivo", command=self.establecer_contrasena_archivo)
        establecer_contrasena_button.grid(row=6, column=0, columnspan=5, padx=10, pady=10)

        generar_contrasena_button = tk.Button(self, text="Generar Contraseña", command=self.generar_contrasena)
        generar_contrasena_button.grid(row=4, column=3, padx=10, pady=10)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        try:
            with open("usuarios.csv", "r") as file:
                reader = csv.reader(file)
                data = list(reader)

            # Eliminar las filas existentes en la tabla
            self.tabla.delete(*self.tabla.get_children())

            # Agregar los datos del archivo CSV a la tabla
            for row in data:
                self.tabla.insert("", tk.END, values=row)
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo CSV no existe.")

    def agregar_usuario(self):
        nombre = self.nombre_var.get()
        correo = self.correo_var.get()
        contrasena = self.contrasena_var.get()

        if nombre and correo and contrasena:
            with open("usuarios.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([nombre, correo, contrasena])

            self.nombre_var.set("")
            self.correo_var.set("")
            self.contrasena_var.set("")

            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", "Por favor, ingrese todos los campos.")

    def actualizar_usuario(self):
        if self.fila_seleccionada:
            nombre = self.nombre_var.get()
            correo = self.correo_var.get()
            contrasena = self.contrasena_var.get()

            if nombre and correo and contrasena:
                usuarios = self.tabla.get_children()
                index = usuarios.index(self.fila_seleccionada)

                with open("usuarios.csv", "r") as file:
                    reader = csv.reader(file)
                    data = list(reader)

                data[index] = [nombre, correo, contrasena]

                with open("usuarios.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(data)

                self.nombre_var.set("")
                self.correo_var.set("")
                self.contrasena_var.set("")

                self.cargar_usuarios()
                self.fila_seleccionada = None
            else:
                messagebox.showerror("Error", "Por favor, ingrese todos los campos.")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un usuario.")

    def eliminar_usuario(self):
        if self.fila_seleccionada:
            usuarios = self.tabla.get_children()
            index = usuarios.index(self.fila_seleccionada)

            with open("usuarios.csv", "r") as file:
                reader = csv.reader(file)
                data = list(reader)

            del data[index]

            with open("usuarios.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(data)

            self.nombre_var.set("")
            self.correo_var.set("")
            self.contrasena_var.set("")

            self.cargar_usuarios()
            self.fila_seleccionada = None
        else:
            messagebox.showerror("Error", "Por favor, seleccione un usuario.")

    def mostrar_seleccion(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            fila_seleccionada = seleccion[0]
            valores = self.tabla.item(fila_seleccionada)["values"]
            self.nombre_var.set(valores[0])
            self.correo_var.set(valores[1])
            self.contrasena_var.set(valores[2])
            self.fila_seleccionada = fila_seleccionada

    def establecer_contrasena_archivo(self):
        contrasena_archivo = self.contrasena_archivo_var.get()

        if contrasena_archivo:
            with open("contrasena.txt", "w") as file:
                file.write(contrasena_archivo)

            messagebox.showinfo("Éxito", "Contraseña establecida correctamente.")
            self.contrasena_archivo_var.set("")
        else:
            messagebox.showerror("Error", "Por favor, ingrese una contraseña.")

    def generar_contrasena(self):
        longitud = 20
        caracteres = string.ascii_letters + string.digits
        contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
        self.contrasena_var.set(contrasena)

app = LoginApp()
app.mainloop()
