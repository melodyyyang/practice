from staffuser import *
from food import *
from order import *
from id_generator import IdGenerator
import json

class System:
    order_id_generator = IdGenerator()

    def __init__(self):
        self._orders = []
        self._staff = []

        # This will be the list of sides available to the customer
        self._sides = [
            SideFood("Nuggets - 3 pieces"),
            SideFood("Nuggets - 6 pieces"),
            SideFood("Nuggets - 24 deal"),
            SideFood("Fries Small"),
            SideFood("Fries Medium"),
            SideFood("Fries Large"),
            SideFood("Coke Small"),
            SideFood("Coke Medium")
        ]

        # This will be the list of toppings available to the customer
        self._toppings = [
            Topping("Tomato"),
            Topping("Cheddar Cheese"),
            Topping("Swiss Cheese"),
            Topping("Lettuce"),
            Topping("Tomato Sauce")
        ]

        self._staff.append(StaffUser("jlam", "Jonathan", "123"))
        self._staff.append(StaffUser("mel", "Melody", "abc"))
        self._staff.append(StaffUser("lust", "Lucius", "qwerty"))
        
        self._stock = {
            # Mains
            "Wrap": 20,
            "Sesame Bun": 10,
            "Muffin Bun": 10,
            "Chicken Patty": 4,
            "Vegetarian Patty": 5,
            "Beef Patty": 4,
            
            # Toppings
            "Tomato": 14,
            "Cheddar Cheese": 14,
            "Swiss Cheese": 14,
            "Lettuce": 14,
            "Tomato Sauce": 14,
           
            # Sides
            "Nuggets": 25,
            "Fries": 200,
            "Coke Small": 5,
            "Coke Medium": 3
        }

    @property
    def orders(self):
        return self._orders

    @property
    def staff(self):
        return self._staff

    @property
    def sides(self):
        return self._sides
        
    @property
    def toppings(self):
        return self._toppings
        
    def getStock(self, name):
        ''' Returns the amount of stock available
        for a provided item name
        '''
        return self._stock[name]

    def setStock(self, name, num=0, delta=0):
        ''' Updates the stock of a particular food item.
        There are two ways to call this function.
        Either specify the exact amount using the _num_
        parameter. e.g. if a staff is doing a stocktake
        on amount of food.
        Alternatively, use the _delta_ parameter and this
        will subtract the value of delta from the current
        stock. For example, if delta=3, this will subtract
        3 from the stock.
        '''
        if num != 0:
            self._stock[name] = num
        elif delta != 0:
            self._stock[name] -= delta
            
    def checkValidStock(self, food_item):
        ''' Given a OrderItem food_item, will return no
        value if there is sufficient stock of all
        buns, patties, toppings and sides.
        Will raise an error otherwise
        '''
        name_to_check = food_item.name
        
        # Burgers - check if buns are available
        if name_to_check == 'Burger':
            if self.getStock(food_item.bunType) < food_item.bunCount:
                raise ValueError

        # Check if there is sufficient (at least one) wrap
        if name_to_check == 'Wrap':
            if self.getStock(name_to_check) < 1:
                raise ValueError

        # Check if toppings and patties avaiable
        if name_to_check == 'Burger' or name_to_check == 'Wrap':
            for topping in food_item.toppings:
                if self.getStock(topping.name) < food_item.stock_cost:
                    raise ValueError
            return
        
        # Treats Nuggets3p, Nuggets6p, and Nuggets24p the same
        if 'Nuggets' in name_to_check:
            if self.getStock('Nuggets') < food_item.stock_cost:
                raise ValueError
            return
            
        # Treats small, medium and large fries the same
        if 'Fries' in name_to_check:
            if self.getStock('Fries') < food_item.stock_cost:
                raise ValueError
            return
        
        # For all other sides
        if self.getStock(name_to_check) < food_item.stock_cost:
            raise ValueError
            
    def updateStock(self, food_item):
        ''' Updates the stock of a food item.
        For burgers and wraps, it will also
        update the stock of its constituent
        toppings and patties.
        '''
        name_to_check = food_item.name
        
        # Burgers - check if buns and toppings available
        if name_to_check == 'Burger':
            self.setStock(food_item.bunType, delta=food_item.bunCount)

        if name_to_check == 'Burger' or name_to_check == 'Wrap':
            for topping in food_item.toppings:
                self.setStock(topping.name, delta=1)
            return
        
        if 'Nuggets' in name_to_check:
            self.setStock('Nuggets', delta=food_item.stock_cost)
            return
            
        if 'Fries' in name_to_check:
            self.setStock('Fries', delta=food_item.stock_cost)
            return
        
        # Sides, Wraps
        self.setStock(name_to_check, delta=food_item.stock_cost)
        
    def addOrder(self, order):
        ''' Adds a provided Order _order_ to the
        System.
        '''
        # Validation
        for food_item in order.mains:
            self.checkValidStock(food_item)
        for food_item in order.sides:
            self.checkValidStock(food_item)

        # Update stock
        for food_item in order.mains:
            self.updateStock(food_item)
        for food_item in order.sides:
            self.updateStock(food_item)
        
        # Now that the order has been confirmed and verified,
        # we can assign an ID to it.
        order.setId(System.order_id_generator.next())
        self._orders.append(order)
        
    def getOrder(self, order_id):
        """ Gets an order that matches a
        given order_id. This uses a linear search,
        though a binary search, or hash map would
        be more efficient for real-world implementations.
        """
        for order in self._orders:
            if order.id == order_id:
                return order
                
        
    def removeOrder(self, order_id):
        """ Removes an order that matches a
        given order_id. This uses a linear search,
        though a binary search, or hash map would
        be more efficient for real-world implementations.
        """
        for order in self._orders:
            if order.id == order_id:
                self._orders.remove(order)
                return
                
    def does_username_exist(self, username):
        ''' Checks if a provided username exists in the staff list'''
        for staff in self._staff:
            if staff.username == username:
                return True
        return False

    '''
    Returns a readable format of the current orders which
    can be passed into the front-end system
    def json_orders_current(self):
        return [
            o.dict() for o in self._orders
            if o.status != 'Completed'
        ]

    # For archive purposes
    def json_orders_completed(self):
        return [
            o.dict() for o in self._orders
            if o.status == 'Completed'
        ]

    def view_current_orders(self):
        # Returns a human-readable JSON representation
        json_object = self.json_orders_current()
        return json.dumps(json_object)
        
    def view_completed_orders(self):
        # Returns a human-readable JSON representation
        json_object = self.json_orders_completed()
        return json.dumps(json_object)
    '''
