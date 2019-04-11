from src.order import OrderItem

class Topping:
    toppings = {
        "Chicken Patty": 0.4,
        "Vegetarian Patty": 0.5,
        "Beef Patty": 0.4,
        "Tomato": 0.1,
        "Cheddar Cheese": 0.15,
        "Swiss Cheese": 0.15,
        "Tomato Sauce": 0.05,
        "Lettuce": 0.05,
    }
    
    def __init__(self, name):
        self._name = name
        self._price = Topping.toppings[name]

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    def dict(self):
        return {
            "name": self._name,
            "price": self._price,
        }

class SideFood(OrderItem):
    ''' The sides_options format stores the
    name of the side food as the dictionary
    key, and a 2-tuple as its value.
    The tuple contains the price as its first
    value, and its unit of deductable quantity in the
    second value.
    For example, nuggets are measured in integer
    quantities, so a Nuggets3p will subtract 3
    from the total amount of nuggets.
    Fries are measured in grams, so a small fries
    will subtract 75g.
    Drinks are stored in amount of bottles,
    so consuming a small coke will deduct 1
    from the amount of coke cans.
    '''
    sides_options = {
        "Nuggets - 3 pieces": (3.5, 3),
        "Nuggets - 6 pieces": (6, 6),
        "Nuggets - 24 deal": (9.95, 24),
        "Fries Small": (2, 75),
        "Fries Medium": (3, 125),
        "Fries Large": (4, 210),
        "Coke Small": (2, 1),
        "Coke Medium": (3, 1)
    }

    def __init__(self, name):
        super(SideFood, self).__init__(name,
                                       SideFood.sides_options[name][0],
                                       "Side",
                                       SideFood.sides_options[name][1])