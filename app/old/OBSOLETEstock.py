class Stock:

    def __init__(self, name, amount):
        self._name = name
        self._amount = amount

    def setAmount(self, amount):
        self._amount = amount

    def validate(self, amount):
        try:
            amount = int(amount)
        except ValueError:
            print("Non-numeric value")
        try:
            amount >= 0
        except ValueError:
            print("Non-negative values only")
        return True

    @property
    def name(self):
        return self._name

    @property
    def amount(self):
        return self._amount
