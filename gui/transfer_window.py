from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox
from account import SavingAccount

class TransferWindow(QWidget):
    def __init__(self, checking, savings, main_window):
        super().__init__()
        self.setWindowTitle("Transfer")
        self.setFixedSize(350, 300)
        self.checking = checking
        self.savings = savings
        self.main_window = main_window

        layout = QVBoxLayout()

        # Return button
        return_btn = QPushButton("← Return")
        return_btn.clicked.connect(self.go_back)
        layout.addWidget(return_btn)

        # Title
        title = QLabel("<h2>Transfer</h2>")
        layout.addWidget(title)

        # To account dropdown
        self.to_label = QLabel("To:")
        self.to_combo = QComboBox()
        self.to_combo.addItems([self.checking.get_name(), self.savings.get_name()])
        self.to_combo.setCurrentIndex(1)
        self.to_combo.currentIndexChanged.connect(self.update_from_and_placeholder)
        layout.addWidget(self.to_label)
        layout.addWidget(self.to_combo)

        # From account label (auto-filled)
        self.from_label = QLabel()
        layout.addWidget(self.from_label)

        # Amount input
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)

        # OK button
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.transfer)
        layout.addWidget(ok_btn)

        self.setLayout(layout)
        self.update_from_and_placeholder()

    def update_from_and_placeholder(self):
        if self.to_combo.currentIndex() == 0:
            self.from_account = self.savings
            self.to_account = self.checking
        else:
            self.from_account = self.checking
            self.to_account = self.savings

        self.from_label.setText(f"From: {self.from_account.get_name()}")

        if isinstance(self.from_account, SavingAccount):
            max_amount = max(0, self.from_account.get_balance() - self.from_account.MINIMUM)
        else:
            max_amount = self.from_account.get_balance()

        self.amount_input.setPlaceholderText(f"Max: {max_amount:.2f}")

    def transfer(self):
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter a valid number.")
            self.amount_input.clear()
            return

        if amount <= 0:
            QMessageBox.warning(self, "Error", "Amount must be positive.")
            self.amount_input.clear()
            return

        if isinstance(self.from_account, SavingAccount):
            max_amount = max(0, self.from_account.get_balance() - self.from_account.MINIMUM)
        else:
            max_amount = self.from_account.get_balance()

        if amount > max_amount:
            QMessageBox.warning(self, "Error", "Insufficient funds or would drop below minimum.")
            self.amount_input.clear()
            return

        self.from_account.withdraw(amount)
        self.to_account.deposit(amount)

        self.amount_input.clear()
        self.main_window.update_balances()
        QMessageBox.information(self, "Success", f"Transferred ${amount:.2f} from {self.from_account.get_name()} to {self.to_account.get_name()}.")

    def go_back(self):
        self.close()
        self.main_window.setEnabled(True)
        self.main_window.update_balances()
