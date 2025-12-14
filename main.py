from PyQt6.QtWidgets import QApplication
from account import Account, SavingAccount
from gui.main_window import MainWindow
import sys

def main():
    checking = Account("Checking", filename="data/checking.csv", initial_balance=50)
    savings = SavingAccount("Savings", filename="data/savings.csv")

    app = QApplication(sys.argv)
    window = MainWindow(checking, savings)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
