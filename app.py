import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QStackedWidget, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QFormLayout, QDialog
)
import requests

user_name = None
password = None

host = "127.0.0.1:5000"


class MainPageWidget(QWidget):
    def __init__(self, switch_to_sign_in, switch_to_register, switch_to_delete):
        super().__init__()
        self.switch_to_sign_in = switch_to_sign_in
        self.switch_to_register = switch_to_register
        self.switch_to_delete = switch_to_delete
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Welcome Label
        welcome_label = QLabel("Welcome! Please choose an option:")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Buttons for Sign In and Register
        sign_in_button = QPushButton("Sign In", self)
        register_button = QPushButton("Register", self)
        remove_button = QPushButton("Delete Account", self)

        # Connect buttons to corresponding methods
        sign_in_button.clicked.connect(self.switch_to_sign_in)
        register_button.clicked.connect(self.switch_to_register)
        remove_button.clicked.connect(self.switch_to_delete)

        # Add buttons to the layout
        layout.addWidget(sign_in_button)
        layout.addWidget(register_button)
        layout.addWidget(remove_button)

        self.setLayout(layout)


class SignInWidget(QWidget):
    def __init__(self, show_main_page ,switch_to_forgot_password, switch_to_ledger, get_id_pwd):
        super().__init__()
        self.switch_to_forgot_password = switch_to_forgot_password
        self.show_main_page = show_main_page
        self.switch_to_ledger = switch_to_ledger
        self.get_id_pwd = get_id_pwd
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("Sign In")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # ID Field
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("Enter your ID")
        layout.addWidget(self.id_input)

        # Password Field
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter your Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Login Button
        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        # Forgot Password Button
        forgot_password_button = QPushButton("Forgot Password?", self)
        forgot_password_button.clicked.connect(self.switch_to_forgot_password)
        layout.addWidget(forgot_password_button)
        
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.show_main_page)
        layout.addWidget(back_button)

        self.setLayout(layout)
        
    def login(self):
        user_id = self.id_input.text()
        password = self.password_input.text()

        if not user_id or not password:
            QMessageBox.warning(self, 'Error', 'User ID and password are required')
            return

        url = 'http://127.0.0.1:30000/api/login'
        data = {'id': user_id, 'pwd': password}

        try:
            response = requests.get(url, json=data)
            if response.json()['status'] == 200:
                QMessageBox.information(self, 'Success', 'Login successful')
                self.get_id_pwd(user_id, password)
                self.switch_to_ledger()
            elif response.json()['status'] == 209:
                QMessageBox.information(self, ':((', 'Invalid Credentials')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')


class RegisterWidget(QWidget):
    def __init__(self, switch_to_main_page):
        super().__init__()
        self.switch_to_main_page = switch_to_main_page
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        layout.addWidget(QLabel("Register Page"))
        
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.id_input)
        
        self.pwd_input = QLineEdit(self)
        self.pwd_input.setPlaceholderText("Enter your password")
        layout.addWidget(self.pwd_input)
        
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter your Email")
        layout.addWidget(self.email_input)
        
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Enter your Phone Number")
        layout.addWidget(self.phone_input)
        
        register_button = QPushButton("Register", self)
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.switch_to_main_page)
        layout.addWidget(back_button)

        self.setLayout(layout)
        
    def register(self):
        user_id = self.id_input.text()
        password = self.pwd_input.text()
        email = self.email_input.text()
        mobile = self.phone_input.text()

        if not user_id or not password or not email or not mobile:
            QMessageBox.warning(self, 'Error', 'Details are required')
            return

        url = 'http://127.0.0.1:30000/api/register'
        data = {'id': user_id, 'pwd': password, 'email' : email, 'mobile' : mobile}

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
        
class ForgotPasswordWidget(QWidget):
    def __init__(self, swicth_to_SignIn):
        super().__init__()
        self.switch_to_sign_in = swicth_to_SignIn
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("Forgot Password")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # ID Field
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("Enter your ID")
        layout.addWidget(self.id_input)

        self.pwd_input = QLineEdit(self)
        self.pwd_input.setPlaceholderText("Enter the new password")
        layout.addWidget(self.pwd_input)
        
        # Code Field
        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText("Enter the code sent to your email")
        layout.addWidget(self.code_input)
        
        # Send Code Button
        send_code_button = QPushButton("Send Code to Email", self)
        send_code_button.clicked.connect(self.send_code)  # Action to send the code
        layout.addWidget(send_code_button)

        # Reset Password Button
        reset_password_button = QPushButton("Change Password", self)
        reset_password_button.clicked.connect(self.pwd_reset)  # Action to reset the password
        layout.addWidget(reset_password_button)
        
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.switch_to_sign_in)
        layout.addWidget(back_button)


        self.setLayout(layout)
        
    def send_code(self):
        user_id = self.id_input.text()

        if not user_id:
            QMessageBox.warning(self, 'Error', 'Details are required')
            return

        url = 'http://127.0.0.1:30000/api/send_code'
        data = {'id': user_id}

        try:
            response = requests.get(url, json=data)
            if response.json()['status'] == 200:
                QMessageBox.information(self, 'Success', 'Code sent successfully')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
            
    def pwd_reset(self):
        user_id = self.id_input.text()
        code = self.code_input.text()
        pwd = self.pwd_input.text()

        if not user_id or not code:
            QMessageBox.warning(self, 'Error', 'Details are required')
            return

        url = 'http://127.0.0.1:30000/api/pwd_reset'
        data = {'id': user_id,'new_pwd' : pwd, 'code' : code}

        try:
            response = requests.post(url, json=data)
            if response.json()['status'] == 200:
                QMessageBox.information(self, 'Success', 'Password Changed successfully')
            elif response.json()['status'] == 409:
                QMessageBox.information(self, ':((', 'Wrong Code')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')


class BalanceWidget(QWidget):
    def __init__(self, switch_to_signin, user_id, user_pwd):
        super().__init__()
        self.switch_to_signin = switch_to_signin
        self.user_id = user_id
        self.user_pwd = user_pwd
        self.balances = requests.get("http://127.0.0.1:30000/api/get_data", json = {'id' : self.user_id, 'pwd' : self.user_pwd}).json()['data']
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        # Title
        title_label = QLabel("Balances")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Table Widget to Display Balances
        self.table = QTableWidget()
        self.table.setRowCount(len(self.balances))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Balance"])
        self.populate_table()
        layout.addWidget(self.table)

        # Logout Button
        logout_button = QPushButton("Logout", self)
        logout_button.clicked.connect(self.switch_to_signin)
        layout.addWidget(logout_button)

        # Debit and Credit Buttons
        debit_button = QPushButton("Debit", self)
        debit_button.clicked.connect(lambda: self.open_transaction_dialog("Debit"))
        layout.addWidget(debit_button)

        credit_button = QPushButton("Credit", self)
        credit_button.clicked.connect(lambda: self.open_transaction_dialog("Credit"))
        layout.addWidget(credit_button)
        
        add_user_button = QPushButton("Add Person", self)
        add_user_button.clicked.connect(self.add_user)
        layout.addWidget(add_user_button)
        
        del_user_button = QPushButton("Delete Person", self)
        del_user_button.clicked.connect(self.del_user)
        layout.addWidget(del_user_button)

        self.setLayout(layout)

    def populate_table(self):
        self.table.setRowCount(len(self.balances))
        for row, (name, balance) in enumerate(self.balances.items()):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(f"${balance:.2f}"))

    def open_transaction_dialog(self, transaction_type):
        dialog = TransactionDialog(transaction_type, self.balances, self.update_balances, self.user_id, self.user_pwd)
        dialog.exec_()
        

    def update_balances(self):
        self.balances = requests.get("http://127.0.0.1:30000/api/get_data", json = {'id' : self.user_id, 'pwd' : self.user_pwd}).json()['data']
        self.populate_table()
        
    def add_user(self):
        dialog = ADD_user(self.user_id, self.user_pwd)
        dialog.exec_()
        self.update_balances()
        
    def del_user(self):
        dialog = del_user(self.user_id, self.user_pwd)
        dialog.exec_()
        self.update_balances()
        
class ADD_user(QDialog):
    def __init__(self, user_id, user_pwd):
        self.user_id = user_id
        self.user_pwd = user_pwd
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(f"Add Person")
        self.resize(300, 150)

        layout = QFormLayout()
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        layout.addRow("Name:", self.name_input)
        
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter amount")
        layout.addRow("Amount:", self.amount_input)
        
        submit_button = QPushButton(f"Submit", self)
        submit_button.clicked.connect(self.add_user)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        
    def add_user(self):
        response = requests.put("http://127.0.0.1:30000/api/add_user", json = {'id' : self.user_id, 'pwd' : self.user_pwd, 'name' : self.name_input.text(), 'data' : self.amount_input.text()})
        self.accept()


class del_user(QDialog):
    def __init__(self, user_id, user_pwd):
        self.user_id = user_id
        self.user_pwd = user_pwd
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(f"Remove Person")
        self.resize(300, 150)

        layout = QFormLayout()
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        layout.addRow("Name:", self.name_input)
        
        submit_button = QPushButton(f"Submit", self)
        submit_button.clicked.connect(self.add_user)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        
    def add_user(self):
        response = requests.delete("http://127.0.0.1:30000/api/rm_user", json = {'id' : self.user_id, 'pwd' : self.user_pwd, 'name' : self.name_input.text()})
        self.accept()


class TransactionDialog(QDialog):
    def __init__(self, transaction_type, balances, update_callback, user_id, user_pwd):
        super().__init__()
        self.transaction_type = transaction_type
        self.balances = balances
        self.update_callback = update_callback
        self.user_id = user_id
        self.user_pwd = user_pwd
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"{self.transaction_type} Amount")
        self.resize(300, 150)

        layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        layout.addRow("Name:", self.name_input)
        
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter amount")
        layout.addRow("Amount:", self.amount_input)

        submit_button = QPushButton(f"{self.transaction_type}", self)
        submit_button.clicked.connect(self.process_transaction)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def process_transaction(self):
        name = self.name_input.text().strip()
        amount_text = self.amount_input.text().strip()

        if not name or not amount_text:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount!")
            return

        if name not in self.balances:
            QMessageBox.warning(self, "Error", f"Name '{name}' not found!")
            return

        if self.transaction_type == "Debit":
            self.balances[name] -= amount
            self.add_txn(self.user_id, name, -1*int(amount_text), self.user_pwd)
        elif self.transaction_type == "Credit":
            self.add_txn(self.user_id, name, int(amount_text), self.user_pwd)
            self.balances[name] += amount

        self.update_callback()
        self.accept()
        
    def add_txn(self, user_id, name, amount, pwd):
        url = 'http://127.0.0.1:30000/api/add_txn'
        data = {'id': user_id,'pwd' : pwd,'name' : name, 'data' : amount}

        try:
            response = requests.put(url, json=data)
            if response.json()['status'] == 409:
                QMessageBox.information(self, ':((', 'Wrong Password')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
            
class Delete_Account(QWidget):
    def __init__(self, switch_to_main_page):
        super().__init__()
        self.switch_to_main_page = switch_to_main_page
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        layout.addWidget(QLabel("Delete Page"))
        
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("Enter your ID")
        layout.addWidget(self.id_input)
        
        self.pwd_input = QLineEdit(self)
        self.pwd_input.setPlaceholderText("Enter your password")
        layout.addWidget(self.pwd_input)
        
        register_button = QPushButton("Delete", self)
        register_button.clicked.connect(self.delete)
        layout.addWidget(register_button)

        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.switch_to_main_page)
        layout.addWidget(back_button)

        self.setLayout(layout)
        
    def delete(self):
        user_id = self.id_input.text()
        password = self.pwd_input.text()

        if not user_id or not password:
            QMessageBox.warning(self, 'Error', 'Details are required')
            return

        url = 'http://127.0.0.1:30000/api/rm_acc'
        data = {'id': user_id, 'pwd': password}

        try:
            response = requests.delete(url, json=data)
            if response.json()['status'] == 200:
                QMessageBox.information(self, 'Success', 'Account Deleted successfully')
            elif response.json()['status'] == 409:
                QMessageBox.information(self, ':((', 'Wrong Password')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('message'))
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login and Register System")

        # Stacked Widget for navigation
        self.stack = QStackedWidget()
        self.user_id = None
        self.user_pwd = None

        # Widgets for Main Page, Sign In, and Register
        self.main_page_widget = MainPageWidget(self.show_sign_in, self.show_register, self.show_del_acc_page)
        self.sign_in_widget = SignInWidget(self.show_main_page, self.show_forgot_pwd, self.show_ledger, self.get_id_pwd)
        self.register_widget = RegisterWidget(self.show_main_page)
        self.forgot_pwd_widget = ForgotPasswordWidget(self.show_sign_in)
        self.delete_acc_widget = Delete_Account(self.show_main_page)
        
        self.stack.addWidget(self.main_page_widget)
        self.stack.addWidget(self.sign_in_widget)  
        self.stack.addWidget(self.register_widget)   
        self.stack.addWidget(self.forgot_pwd_widget)
        self.stack.addWidget(self.delete_acc_widget)
        

        self.setCentralWidget(self.stack)
        self.stack.setCurrentWidget(self.main_page_widget)

    def show_main_page(self):
        self.stack.setCurrentWidget(self.main_page_widget)

    def show_sign_in(self):
        self.stack.setCurrentWidget(self.sign_in_widget)

    def show_register(self):
        self.stack.setCurrentWidget(self.register_widget)
        
    def show_forgot_pwd(self):
        self.stack.setCurrentWidget(self.forgot_pwd_widget)
        
    def show_ledger(self):
        self.ledger_widget = BalanceWidget(self.show_sign_in, self.user_id, self.user_pwd)
        self.stack.addWidget(self.ledger_widget)
        self.stack.setCurrentWidget(self.ledger_widget)
        
    def get_id_pwd(self, id, pwd):
        self.user_id = id
        self.user_pwd = pwd
        
    def show_del_acc_page(self):
        self.stack.setCurrentWidget(self.delete_acc_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
