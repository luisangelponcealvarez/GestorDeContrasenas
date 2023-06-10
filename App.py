import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import random
import string


class RegistroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro de Usuarios")

        # Crear variables para almacenar los datos ingresados
        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()

        # Conectar a la base de datos SQLite
        self.conexion = sqlite3.connect("usuarios.db")
        self.crear_tabla()

        # Crear la tabla para mostrar los datos
        self.tabla = ttk.Treeview(self, columns=("Nombre", "Correo", "Contraseña"), show="headings")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Contraseña", text="Contraseña")
        self.tabla.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

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

        # Cargar los datos desde la base de datos
        self.cargar_datos()

    def crear_tabla(self):
        cursor = self.conexion.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT, correo TEXT, contrasena TEXT)")
        self.conexion.commit()

    def cargar_datos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT nombre, correo, contrasena FROM usuarios")
        rows = cursor.fetchall()
        for row in rows:
            self.tabla.insert("", "end", values=row)

    def guardar_datos(self):
        nombre = self.nombre_var.get()
        correo = self.correo_var.get()
        contrasena = self.contrasena_var.get()

        if nombre and correo and contrasena:
            # Agregar los datos a la tabla
            self.tabla.insert("", "end", values=(nombre, correo, contrasena))
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Datos guardados correctamente.")

            # Guardar los datos en la base de datos
            cursor = self.conexion.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, correo, contrasena) VALUES (?, ?, ?)",
                           (nombre, correo, contrasena))
            self.conexion.commit()
        else:
            messagebox.showerror("Error", "Por favor, rellene todos los campos.")

    def limpiar_campos(self):
        self.nombre_var.set("")
        self.correo_var.set("")
        self.contrasena_var.set("")

        # Ocultar la contraseña en el campo de entrada
        self.contrasena_entry.config(show="*")

    def buscar_datos(self):
        termino = self.buscar_entry.get()
        if termino:
            # Buscar los datos en la base de datos
            cursor = self.conexion.cursor()
            cursor.execute("SELECT nombre, correo, contrasena FROM usuarios WHERE LOWER(nombre) LIKE ? OR LOWER(correo) LIKE ?",
                           ('%' + termino.lower() + '%', '%' + termino.lower() + '%'))
            rows = cursor.fetchall()
            self.mostrar_resultados(rows)
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un término de búsqueda.")

    def mostrar_resultados(self, resultados):
        # Crear una ventana emergente para mostrar los resultados de la búsqueda
        ventana_resultados = tk.Toplevel(self)
        ventana_resultados.title("Resultados de Búsqueda")

        if resultados:
            # Crear una tabla para mostrar los resultados
            tabla_resultados = ttk.Treeview(ventana_resultados, columns=("Nombre", "Correo", "Contraseña"), show="headings")
            tabla_resultados.heading("Nombre", text="Nombre")
            tabla_resultados.heading("Correo", text="Correo")
            tabla_resultados.heading("Contraseña", text="Contraseña")
            tabla_resultados.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            for row in resultados:
                tabla_resultados.insert("", "end", values=row)

            # Botones para copiar los datos seleccionados
            copiar_nombre_button = tk.Button(ventana_resultados, text="Copiar Nombre", command=lambda: self.copiar_dato_seleccionado(tabla_resultados, 0))
            copiar_nombre_button.grid(row=1, column=0, padx=1, pady=5)

            copiar_correo_button = tk.Button(ventana_resultados, text="Copiar Correo", command=lambda: self.copiar_dato_seleccionado(tabla_resultados, 1))
            copiar_correo_button.grid(row=2, column=0, padx=2, pady=5)

            copiar_contrasena_button = tk.Button(ventana_resultados, text="Copiar Contraseña", command=lambda: self.copiar_dato_seleccionado(tabla_resultados, 2))
            copiar_contrasena_button.grid(row=3, column=0, padx=3, pady=5)
        else:
            mensaje_label = tk.Label(ventana_resultados, text="No se encontraron resultados.")
            mensaje_label.grid(row=1, column=0, padx=5, pady=5)

    def copiar_dato_seleccionado(self, tabla, columna):
        # Obtener el índice de la fila seleccionada
        seleccion = tabla.selection()
        if seleccion:
            # Obtener el valor de la columna seleccionada
            valor = tabla.item(seleccion[0])["values"][columna]
            if valor:
                # Copiar el dato al portapapeles
                self.clipboard_clear()
                self.clipboard_append(valor)
                messagebox.showinfo("Éxito", "Dato copiado al portapapeles.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una fila.")

    def generar_contrasena(self):
        longitud = 20
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
        self.contrasena_var.set(contrasena)


if __name__ == "__main__":
    app = RegistroApp()
    app.mainloop()
