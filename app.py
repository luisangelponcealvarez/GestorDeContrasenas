import string
import random
import tkinter as tk
from tkinter import filedialog

window = tk.Tk()
window.title("Gestor de Contraseñas")
window.geometry("400x400")  # Tamaño de la ventana aumentado

input_width = int(window.winfo_width() * 60.0)  # Ancho de los elementos de entrada de texto

class PasswordManager:
    def __init__(self):
        self.passwords = {}

    def add_password(self, service, password):
        self.passwords[service] = password

    def get_password(self, service):
        return self.passwords.get(service, "Contraseña no encontrada")

    def generate_password(self, length=10):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password


def add_password():
    service = service_entry.get()
    password = password_entry.get()
    password_manager.add_password(service, password)
    result_entry.delete(0, tk.END)
    result_entry.insert(tk.END, "Contraseña guardada con éxito.")


def get_password():
    service = service_entry.get()
    password = password_manager.get_password(service)
    result_entry.delete(0, tk.END)
    result_entry.insert(tk.END, password)


def generate_password():
    length = int(length_entry.get())
    password = password_manager.generate_password(length)
    result_entry.delete(0, tk.END)
    result_entry.insert(tk.END, password)


def save_passwords():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as file:
            for service, password in password_manager.passwords.items():
                file.write(f"{service}: {password}\n")
        result_entry.delete(0, tk.END)
        result_entry.insert(tk.END, "Contraseñas guardadas en el archivo.")


password_manager = PasswordManager()

service_label = tk.Label(window, text="Servicio:")
service_label.pack()
service_entry = tk.Entry(window, width=input_width)  # Ancho ajustado al 99%
service_entry.pack()

password_label = tk.Label(window, text="Contraseña:")
password_label.pack()
password_entry = tk.Entry(window, show="*", width=input_width)  # Ancho ajustado al 99%
password_entry.pack()

add_button = tk.Button(window, text="Agregar Contraseña", command=add_password)
add_button.pack()

get_button = tk.Button(window, text="Obtener Contraseña", command=get_password)
get_button.pack()

length_label = tk.Label(window, text="Longitud de la Contraseña:")
length_label.pack()
length_entry = tk.Entry(window, width=input_width)  # Ancho ajustado al 99%
length_entry.pack()

generate_button = tk.Button(window, text="Generar Contraseña", command=generate_password)
generate_button.pack()

save_button = tk.Button(window, text="Guardar Contraseñas", command=save_passwords)
save_button.pack()

result_entry = tk.Entry(window, width=input_width)  # Ancho ajustado al 99%
result_entry.pack()

window.mainloop()
