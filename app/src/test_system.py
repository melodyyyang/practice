import pytest
from staffuser import *
from food import *
from order import *
from system import *
from id_generator import IdGenerator


class TestSystem():
    def setup_class(self):
        self.system = System()

    def test_system_setup(self):
        s = self.system
        assert len(s.staff) == 3
        assert len(s.toppings) == 5
        assert len(s.sides) == 8

        assert s.toppings[0].name == "Tomato"
        assert s.toppings[0].price == 0.1
        assert s.toppings[1].name == "Cheddar Cheese"
        assert s.toppings[1].price == 0.15
        assert s.toppings[2].name == "Swiss Cheese"
        assert s.toppings[2].price == 0.15
        assert s.toppings[3].name == "Lettuce"
        assert s.toppings[3].price == 0.05
        assert s.toppings[4].name == "Tomato Sauce"
        assert s.toppings[4].price == 0.05
        
        assert s.sides[0].name == "Nuggets - 3 pieces"
        assert s.sides[0].price == 3.5

    def test_burger_creation(self):
        s = self.system
        b = Burger()
        b.setBunType("Sesame Bun")
        b.setBunCount(2)
        assert b.price == 10
        assert b.name == "Burger"
        assert b.bunType == "Sesame Bun"
        assert b.bunCount == 2
        
        # Adding Topping(Lettuce) to Burger
        b.addTopping(Topping("Lettuce"))
        assert len(b.toppings) == 1
        assert b.toppings[0].name == "Lettuce"
        assert b.toppings[0].price == 0.05
        assert b.price == 10.05

        # Adding Topping(Tomato) to Burger
        b.addTopping(Topping("Tomato"))
        assert len(b.toppings) == 2
        assert b.toppings[1].name == "Tomato"
        assert b.toppings[1].price == 0.1
        assert b.price == 10.15

        # Test removing toppings
        b.removeTopping("Tomato")
        assert len(b.toppings) == 1
        assert b.price == 10.05     

    def test_order_creation(self):
        s = self.system
        b = Burger()
        b.setBunType("Sesame Bun")
        b.setBunCount(2)
        b.addTopping(Topping("Lettuce"))

        # Test adding Mains and Sides to Order
        o = Order()
        o.addMain(b)
        assert o.price == 10.05
        o.addSide(SideFood("Nuggets - 3 pieces"))
        assert o.price == 13.55
        o.addSide(SideFood("Nuggets - 6 pieces"))
        assert o.price == 19.55
        o.addSide(SideFood("Coke Small"))
        assert o.price == 21.55
        #print(o)
        
        ###
        o2 = Order()
        w = Wrap()
        w.addTopping(Topping("Tomato"))
        w.addTopping(Topping("Tomato Sauce"))
        w.addTopping(Topping("Cheddar Cheese"))
        assert w.price == 9 + 0.1 + 0.15 + 0.05     
        o2.addMain(w)
        
        # Test stock
        assert s.getStock("Wrap") == 20
        assert s.getStock("Sesame Bun") == 10
        assert s.getStock("Muffin Bun") == 10
        assert s.getStock("Tomato") == 14
        assert s.getStock("Cheddar Cheese") == 14
        assert s.getStock("Swiss Cheese") == 14
        assert s.getStock("Lettuce") == 14
        assert s.getStock("Tomato Sauce") == 14
        assert s.getStock("Nuggets") == 25
        assert s.getStock("Fries") == 200
        assert s.getStock("Coke Small") == 5
        assert s.getStock("Coke Medium") == 3
        assert s.getStock("Chicken Patty") == 4
        assert s.getStock("Vegetarian Patty") == 5
        assert s.getStock("Beef Patty") == 4
        
        # After adding an item to the order
        # check if the stock is updated
        s.addOrder(o)
        assert len(s.orders) == 1
        assert s.getStock("Wrap") == 20
        assert s.getStock("Sesame Bun") == 8
        assert s.getStock("Muffin Bun") == 10
        assert s.getStock("Tomato") == 14
        assert s.getStock("Cheddar Cheese") == 14
        assert s.getStock("Swiss Cheese") == 14
        assert s.getStock("Lettuce") == 13
        assert s.getStock("Tomato Sauce") == 14
        assert s.getStock("Nuggets") == 25-9
        assert s.getStock("Fries") == 200
        assert s.getStock("Coke Small") == 5-1
        assert s.getStock("Coke Medium") == 3
        assert s.getStock("Chicken Patty") == 4
        assert s.getStock("Vegetarian Patty") == 5
        assert s.getStock("Beef Patty") == 4
        
        # After adding an item to the order
        # check if the stock is updated
        s.addOrder(o2)
        assert len(s.orders) == 2
        assert s.getStock("Wrap") == 20
        assert s.getStock("Sesame Bun") == 8
        assert s.getStock("Muffin Bun") == 10
        assert s.getStock("Tomato") == 13
        assert s.getStock("Cheddar Cheese") == 13
        assert s.getStock("Swiss Cheese") == 14
        assert s.getStock("Lettuce") == 13
        assert s.getStock("Tomato Sauce") == 13
        assert s.getStock("Nuggets") == 25-9
        assert s.getStock("Fries") == 200
        assert s.getStock("Coke Small") == 5-1
        assert s.getStock("Coke Medium") == 3
        assert s.getStock("Chicken Patty") == 4
        assert s.getStock("Vegetarian Patty") == 5
        assert s.getStock("Beef Patty") == 4

        # After adding an item to the order
        # check if the stock is updated
        # and check for order price
        o3 = Order()
        o3.addSide(SideFood("Coke Medium"))
        o3.addSide(SideFood("Nuggets - 6 pieces"))
        o3.addSide(SideFood("Fries Medium"))
        # print(o3)
        assert o3.price == 3 + 6 + 3
        s.addOrder(o3)
        assert len(s.orders) == 3
        assert s.getStock("Wrap") == 20
        assert s.getStock("Sesame Bun") == 8
        assert s.getStock("Muffin Bun") == 10
        assert s.getStock("Tomato") == 13
        assert s.getStock("Cheddar Cheese") == 13
        assert s.getStock("Swiss Cheese") == 14
        assert s.getStock("Lettuce") == 13
        assert s.getStock("Tomato Sauce") == 13
        assert s.getStock("Nuggets") == 25-9-6
        assert s.getStock("Fries") == 200-125
        assert s.getStock("Coke Small") == 5-1
        assert s.getStock("Coke Medium") == 3-1
        assert s.getStock("Chicken Patty") == 4
        assert s.getStock("Vegetarian Patty") == 5
        assert s.getStock("Beef Patty") == 4
        

    def test_view_orders(self):
        ''' Test for searching and viewing orders '''
        s = self.system
        view_orders = s.orders
        assert len(view_orders) == 3
        # Staff can view a list of orders

        # Staff can search for orders by id,
        # and update their status e.g. when
        # the order is ready to be picked up
        order_search_1 = s.getOrder(1)
        order_search_2 = s.getOrder(2)
        assert order_search_1.paid == False
        order_search_1.setPaid(True)
        assert order_search_1.status == "Creating"
        order_search_1.setStatus("Cooking")
        assert order_search_1.status == "Cooking"
        order_search_1.setStatus("Ready to pick up")
        assert order_search_1.status == "Ready to pick up"
        order_search_1.setStatus("Collected")
        assert order_search_1.status == "Collected"
        assert order_search_1.price == 21.55
        assert order_search_2.price == 9 + 0.1 + 0.15 + 0.05

    def test_max_two_patty(self):
        b = Burger()
        b.addTopping(Topping("Beef Patty"))
        b.addTopping(Topping("Vegetarian Patty"))
        w = Wrap()
        w.addTopping(Topping("Beef Patty"))
        w.addTopping(Topping("Vegetarian Patty"))
        
        # The next two lines should raise an error
        # if commented out, because you are
        # not allowed more than 2 patties

        # b.addTopping(Topping("Vegetarian Patty"))
        # w.addTopping(Topping("Chicken Patty"))
