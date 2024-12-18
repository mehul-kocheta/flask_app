import webbrowser

# webbrowser.open('https://google.com')  # Go to example.com

import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.user_id_label = QLabel('User ID:')
        self.user_id_input = QLineEdit()
        layout.addWidget(self.user_id_label)
        layout.addWidget(self.user_id_input)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)
        
        self.password_reset_button = QPushButton('Password Reset')
        self.password_reset_button.clicked.connect(self.pwd_reset)
        layout.addWidget(self.password_reset_button)

        self.setLayout(layout)

    def login(self):
        user_id = self.user_id_input.text()
        password = self.password_input.text()

        if not user_id or not password:
            QMessageBox.warning(self, 'Error', 'User ID and password are required')
            return

        url = 'http://127.0.0.1:5000/api/login'
        data = {'id': user_id, 'pwd': password}

        try:
            response = requests.get(url, json=data)
            if response.json()['status'] == 200:
                QMessageBox.information(self, 'Success', 'Login successful')
            elif response.json()['status'] == 209:
                QMessageBox.information(self, ':((', 'Invalid Credentials')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

    def register(self):
        user_id = self.user_id_input.text()
        password = self.password_input.text()

        if not user_id or not password:
            QMessageBox.warning(self, 'Error', 'User ID and password are required')
            return

        url = 'http://127.0.0.1:5000/api/register'
        data = {'id': user_id, 'pwd': password}

        try:
            response = requests.put(url, json=data)
            if response.json()['status'] == 200:
                QMessageBox.information(self, 'Success', 'User registered successfully')
            elif response.json()['status'] == 409:
                QMessageBox.information(self, ':((', 'User already exist')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
            
    def pwd_reset(self):
        user_id = self.user_id_input.text()
        password = self.password_input.text()
        
        if not user_id or not password:
            QMessageBox.warning(self, 'Error', 'User ID and password are required')
            return
        
        url = 'http://127.0.0.1:5000/api/pwd_reset'
        data = {'id': user_id, 'new_pwd': password}
        
        try:
            response = requests.post(url, json=data)
            if response.json()['status'] == 200:
                QMessageBox.information(self, 'Success', 'Password Changed successfully')
            elif response.json()['status'] == 404:
                QMessageBox.information(self, ':((', 'User does not exist')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

