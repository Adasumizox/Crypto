from decimal import Decimal

from blockchain.database import schemas


class Transaction():
    def __init__(self, sender: schemas.User, receiver: schemas.User, amount: float):
        assert amount > 0, "Nice try"
        assert self.sender.balance >= amount, "You cannot overdraft in this system"
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.sender.updateBalance(sender.balance - amount)
        self.receiver.updateBalance(receiver.balance + amount)