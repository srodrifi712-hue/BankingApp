import csv
from datetime import datetime
from typing import List

def save_transaction(filename: str, tx_type: str, amount: float, balance: float) -> None:
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tx_type,
            f"{amount:.2f}",
            f"{balance:.2f}"
        ])

def load_transactions(filename: str) -> List[list]:
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        return []
