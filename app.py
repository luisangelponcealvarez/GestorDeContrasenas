import string
import random
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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


password_manager = PasswordManager()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add_password' in request.form:
            service = request.form['service']
            password = request.form['password']
            password_manager.add_password(service, password)
            message = "Contraseña guardada con éxito."
        elif 'get_password' in request.form:
            service = request.form['service']
            password = password_manager.get_password(service)
            message = password
        elif 'generate_password' in request.form:
            length = int(request.form['length'])
            password = password_manager.generate_password(length)
            message = password
        elif 'save_passwords' in request.form:
            file_path = request.form['file_path']
            with open(file_path, "w") as file:
                for service, password in password_manager.passwords.items():
                    file.write(f"{service}: {password}\n")
            message = "Contraseñas guardadas en el archivo."
        else:
            message = ""
    else:
        message = ""

    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run()
