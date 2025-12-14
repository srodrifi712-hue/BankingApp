from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox

class ActionsWindow(QWidget):
    def __init__(self, account, main_window_ref):
        super().__init__()
        self.account = account
        self.main_window = main_window_ref
        self.setWindowTitle("Actions")
        self.setFixedSize(300, 250)

        layout = QVBoxLayout()

        # Return button
        return_btn = QPushButton("← Return")
        return_btn.clicked.connect(self.go_back)
        layout.addWidget(return_btn)

        layout.addWidget(QLabel("<h2>Actions</h2>"))

        # Input
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        layout.addWidget(self.amount_input)

        # Buttons
        deposit_btn = QPushButton("Deposit")
        withdraw_btn = QPushButton("Withdraw")
        deposit_btn.clicked.connect(self.deposit)
        withdraw_btn.clicked.connect(self.withdraw)
        layout.addWidget(deposit_btn)
        layout.addWidget(withdraw_btn)

        self.setLayout(layout)

    def go_back(self):
        self.close()
        self.main_window.setEnabled(True)
        self.main_window.update_balances()  # refresh balances

    def deposit(self):
        text = self.amount_input.text().strip()
        try:
            amount = float(text)
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter a valid number.")
            self.amount_input.clear()
            return

        if amount <= 0:
            QMessageBox.warning(self, "Error", "Amount must be positive.")
            self.amount_input.clear()
            return

        self.account.deposit(amount)
        self.amount_input.clear()

    def withdraw(self):
        text = self.amount_input.text().strip()
        try:
            amount = float(text)
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter a valid number.")
            self.amount_input.clear()
            return

        if amount <= 0:
            QMessageBox.warning(self, "Error", "Amount must be positive.")
            self.amount_input.clear()
            return

        if not self.account.withdraw(amount):
            QMessageBox.warning(self, "Error", "Insufficient funds or below minimum.")
            self.amount_input.clear()
            return

        self.amount_input.clear()
