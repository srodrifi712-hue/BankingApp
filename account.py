import os
from file_manager import save_transaction, load_transactions
from typing import Optional

class Account:
    def __init__(self, name: str, filename: Optional[str] = None, initial_balance: float = 0):
        self.__name = name
        self._filename = filename or f"data/{name.lower()}.csv"

        if os.path.exists(self._filename):
            transactions = load_transactions(self._filename)
        else:
            transactions = []

        if transactions:
            last_row = transactions[-1]
            try:
                self._balance = float(last_row[3])
            except ValueError:
                self._balance = initial_balance
        else:
            self._balance = initial_balance
            if initial_balance > 0:
                save_transaction(self._filename, "Initial Deposit", initial_balance, self._balance)

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self._balance += amount
        save_transaction(self._filename, "Deposit", amount, self._balance)
        return True

    def withdraw(self, amount: float) -> bool:
        if amount <= 0 or amount > self._balance:
            return False
        self._balance -= amount
        save_transaction(self._filename, "Withdraw", amount, self._balance)
        return True

    def get_balance(self) -> float:
        return self._balance

    def get_name(self) -> str:
        return self.__name


class SavingAccount(Account):
    MINIMUM = 100
    RATE = 0.02

    def __init__(self, name: str, filename: Optional[str] = None):
        # Only start with MINIMUM if file missing/empty
        if filename and os.path.exists(filename):
            transactions = load_transactions(filename)
        else:
            transactions = []

        starting_balance = SavingAccount.MINIMUM if not transactions else 0
        super().__init__(name, filename, initial_balance=starting_balance)
        self._deposit_count = 0

    def deposit(self, amount: float) -> bool:
        success = super().deposit(amount)
        if success:
            self._deposit_count += 1
            if self._deposit_count % 5 == 0:
                self.apply_interest()
        return success

    def apply_interest(self):
        interest = self._balance * SavingAccount.RATE
        self._balance += interest
        save_transaction(self._filename, "Interest", interest, self._balance)

    def withdraw(self, amount: float) -> bool:
        if self._balance - amount < SavingAccount.MINIMUM:
            return False
        return super().withdraw(amount)
