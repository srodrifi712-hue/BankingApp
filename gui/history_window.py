from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from file_manager import load_transactions

class HistoryWindow(QWidget):
    def __init__(self, account, main_window):
        super().__init__()
        self.main_window = main_window
        self.account = account

        self.setWindowTitle("Transaction History")
        self.setFixedSize(450, 300)

        layout = QVBoxLayout()

        return_btn = QPushButton("← Return")
        return_btn.clicked.connect(self.go_back)
        layout.addWidget(return_btn)

        layout.addWidget(QLabel("<h2>Transaction History</h2>"))

        table = QTableWidget()
        transactions = load_transactions(self.account._filename)

        # Show most recent first
        transactions = transactions[::-1]

        table.setRowCount(len(transactions))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Date", "Type", "Amount", "Balance"])

        for row, tx in enumerate(transactions):
            for col, value in enumerate(tx):
                table.setItem(row, col, QTableWidgetItem(value))

        layout.addWidget(table)
        self.setLayout(layout)

    def go_back(self):
        self.close()
        self.main_window.setEnabled(True)
        self.main_window.update_balances()  # refresh balances
