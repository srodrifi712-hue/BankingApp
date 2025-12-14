from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from gui.actions_window import ActionsWindow
from gui.history_window import HistoryWindow
from gui.transfer_window import TransferWindow
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, checking, savings):
        super().__init__()
        self.checking = checking
        self.savings = savings
        self.setWindowTitle("Bank App")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Welcome")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        # Labels for balances
        self.label_checking = QLabel()
        self.label_savings = QLabel()
        self.update_balances()

        # Checking buttons
        btn_check_actions = QPushButton("Actions")
        btn_check_history = QPushButton("View History")
        btn_check_actions.clicked.connect(lambda: self.open_actions(self.checking))
        btn_check_history.clicked.connect(lambda: self.open_history(self.checking))
        layout.addWidget(self.label_checking)
        layout.addWidget(btn_check_actions)
        layout.addWidget(btn_check_history)

        # Savings buttons
        btn_save_actions = QPushButton("Actions")
        btn_save_history = QPushButton("View History")
        btn_save_actions.clicked.connect(lambda: self.open_actions(self.savings))
        btn_save_history.clicked.connect(lambda: self.open_history(self.savings))
        layout.addWidget(self.label_savings)
        layout.addWidget(btn_save_actions)
        layout.addWidget(btn_save_history)

        # Transfer button at the very bottom
        btn_transfer = QPushButton("Transfer")
        btn_transfer.clicked.connect(self.open_transfer)
        layout.addWidget(btn_transfer)

        self.setLayout(layout)

    def update_balances(self):
        self.label_checking.setText(f"Checking Account\nBalance: ${self.checking.get_balance():.2f}")
        self.label_savings.setText(f"Savings Account\nBalance: ${self.savings.get_balance():.2f}")

    def open_actions(self, account):
        self.setEnabled(False)
        self.actions_window = ActionsWindow(account, self)
        self.actions_window.show()

    def open_history(self, account):
        self.setEnabled(False)
        self.history_window = HistoryWindow(account, self)
        self.history_window.show()

    def open_transfer(self):
        self.setEnabled(False)
        self.transfer_window = TransferWindow(self.checking, self.savings, self)
        self.transfer_window.show()
