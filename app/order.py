import json

class Order:
    def __init__(self):
        self._id = 0
        self._price = 0
        self._status = "Creating"
        self._paid = False
        self._mains = []
        self._sides = []
    
    @property
    def id(self):
        return self._id

    def setId(self, id):
        self._id = id

    @property
    def price(self):
        return self._price
        
    @property
    def status(self):
        return self._status
        
    @property
    def paid(self):
        return self._paid
        
    @property
    def mains(self):
        return self._mains
        

    @property
    def sides(self):
        return self._sides
        
    def setStatus(self, status):
        self._status = status
        
    def setPaid(self, paid):
        self._paid = paid
        
    def addMain(self, item):
        self._price += item.price
        self._mains.append(item)
        
    def removeMain(self, item_id):
        for item in self._mains:
            if item.id == item_id:
                self._price -= item.price
                self._mains.remove(item)
        
    def addSide(self, item):
        self._price += item.price
        self._sides.append(item)
        
    def removeSide(self, item_id):
        for item in self._sides:
            if item.id == item_id:
                self._price -= item.price
                self._sides.remove(item)
                
    def dict(self):
        return {
            "id": self._id,
            "price": self._price,
            "status": self._status,
            "paid": self._paid,
            "mains": [food.dict() for food in self._mains],
            "sides": [food.dict() for food in self._sides]
        }
                
    def __str__(self):
        json_object = self.dict()
        return json.dumps(json_object)
                
                
class OrderItem:
    def __init__(self, name, price, type, stock_cost):
        self._name = name
        self._id = 0
        self._price = price
        self._stock_cost = stock_cost
        self._type = type
    
    @property
    def price(self):
        return self._price
        
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def stock_cost(self):
        return self._stock_cost

    def dict(self):
        d = {
            "id": self._id,
            "name": self._name,
            "price": self._price,
            "type": self._type,
        }
        if self._type == 'Main':
            d["toppings"] = [top.dict() for top in self._toppings]
        return d
    
    
    def __str__(self):
        '''Returns a human-readable JSON representation'''
        json_object = self.dict()
        return json.dumps(json_object)

        
        
        
class MainFood(OrderItem):
    def __init__(self, name, base_price):
        self._toppings = []
        self._patty_count = 0
        super(MainFood, self).__init__(name, base_price, "Main", 1)

    def addTopping(self, topping):
        # Checking and updating quantity is not needed
        # here, as this is handled by the system.

        # We can only have max two patties
        if 'Patty' in topping.name:
            if self._patty_count >= 2:
                raise ValueError
            else:
                self._patty_count += 1

        # each ingredient carries an additional price
        self._price += topping.price
        
        self._toppings.append(topping)

    @property
    def toppings(self):
        return self._toppings

    def removeTopping(self, topping_name):
        for topping in self._toppings:
            if topping.name == topping_name:
                # Updating stock is not needed here
                self._price -= topping.price
                self._toppings.remove(topping)
        

        
        
class Burger(MainFood):
    def __init__(self):
        base_price = 10
        self._bunType = ""
        self._bunCount = 0
        
        super(Burger, self).__init__("Burger", base_price)
        
    def setBunType(self, bun):
        self._bunType = bun
        
    def setBunCount(self, count):
        # You are limited to two buns
        if not 0 <= count <= 2:
            raise ValueError
        self._bunCount = count

    @property
    def bunType(self):
        return self._bunType

    @property
    def bunCount(self):
        return self._bunCount

class Wrap(MainFood):
    def __init__(self):
        base_price = 9
        super(Wrap, self).__init__("Wrap", base_price)
