from decimal import Decimal


class User:
    def __init__(self, username: str, password: str, firstName: str, lastName: str):
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.balance: Decimal = Decimal(0)

    def updateBalance(self, balance: Decimal):
        assert (balance >= 0), "You cannot overdraft in this system"
        self.balance = balance