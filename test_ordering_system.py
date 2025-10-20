#!/usr/bin/env python3
"""Tests for the smart ordering system."""

import unittest
from menu import Menu, MenuItem, Category
from order import Order, OrderManager, OrderStatus, OrderItem
from cart import Cart
from ordering_system import OrderingSystem


class TestMenu(unittest.TestCase):
    """Test cases for Menu class."""
    
    def setUp(self):
        self.menu = Menu()
    
    def test_add_item(self):
        """Test adding an item to the menu."""
        item = self.menu.add_item(
            "Test Item",
            "Test Description",
            10.99,
            Category.APPETIZER
        )
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.price, 10.99)
        self.assertTrue(item.available)
    
    def test_get_item(self):
        """Test retrieving an item from the menu."""
        item = self.menu.add_item("Test", "Desc", 5.0, Category.BEVERAGE)
        retrieved = self.menu.get_item(item.id)
        self.assertEqual(retrieved.name, "Test")
    
    def test_get_items_by_category(self):
        """Test filtering items by category."""
        self.menu.add_item("App 1", "Desc", 5.0, Category.APPETIZER)
        self.menu.add_item("App 2", "Desc", 6.0, Category.APPETIZER)
        self.menu.add_item("Main 1", "Desc", 15.0, Category.MAIN_COURSE)
        
        appetizers = self.menu.get_items_by_category(Category.APPETIZER)
        self.assertEqual(len(appetizers), 2)
    
    def test_set_availability(self):
        """Test setting item availability."""
        item = self.menu.add_item("Test", "Desc", 5.0, Category.DESSERT)
        self.assertTrue(item.available)
        
        self.menu.set_availability(item.id, False)
        self.assertFalse(item.available)


class TestCart(unittest.TestCase):
    """Test cases for Cart class."""
    
    def setUp(self):
        self.cart = Cart()
        self.menu = Menu()
        self.item1 = self.menu.add_item("Item 1", "Desc", 10.0, Category.APPETIZER)
        self.item2 = self.menu.add_item("Item 2", "Desc", 15.0, Category.MAIN_COURSE)
    
    def test_add_item(self):
        """Test adding an item to the cart."""
        self.cart.add_item(self.item1, 2)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0].quantity, 2)
    
    def test_add_duplicate_item(self):
        """Test adding the same item twice increases quantity."""
        self.cart.add_item(self.item1, 1)
        self.cart.add_item(self.item1, 2)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0].quantity, 3)
    
    def test_remove_item(self):
        """Test removing an item from the cart."""
        self.cart.add_item(self.item1, 1)
        self.cart.add_item(self.item2, 1)
        self.assertTrue(self.cart.remove_item(self.item1.id))
        self.assertEqual(len(self.cart.items), 1)
    
    def test_get_total(self):
        """Test calculating cart total."""
        self.cart.add_item(self.item1, 2)  # 2 * 10.0 = 20.0
        self.cart.add_item(self.item2, 1)  # 1 * 15.0 = 15.0
        self.assertEqual(self.cart.get_total(), 35.0)
    
    def test_clear_cart(self):
        """Test clearing the cart."""
        self.cart.add_item(self.item1, 1)
        self.cart.clear()
        self.assertTrue(self.cart.is_empty())
    
    def test_get_item_count(self):
        """Test getting total item count."""
        self.cart.add_item(self.item1, 2)
        self.cart.add_item(self.item2, 3)
        self.assertEqual(self.cart.get_item_count(), 5)


class TestOrder(unittest.TestCase):
    """Test cases for Order class."""
    
    def setUp(self):
        self.menu = Menu()
        self.item1 = self.menu.add_item("Item 1", "Desc", 10.0, Category.APPETIZER)
        self.item2 = self.menu.add_item("Item 2", "Desc", 20.0, Category.MAIN_COURSE)
        self.order = Order(1000, "Test Customer", table_number=5)
    
    def test_add_item(self):
        """Test adding an item to an order."""
        self.order.add_item(self.item1, 2)
        self.assertEqual(len(self.order.items), 1)
        self.assertEqual(self.order.items[0].quantity, 2)
    
    def test_remove_item(self):
        """Test removing an item from an order."""
        self.order.add_item(self.item1, 1)
        self.order.add_item(self.item2, 1)
        self.assertTrue(self.order.remove_item(self.item1.id))
        self.assertEqual(len(self.order.items), 1)
    
    def test_get_total(self):
        """Test calculating order total."""
        self.order.add_item(self.item1, 2)  # 20.0
        self.order.add_item(self.item2, 1)  # 20.0
        self.assertEqual(self.order.get_total(), 40.0)
    
    def test_update_status(self):
        """Test updating order status."""
        self.assertEqual(self.order.status, OrderStatus.PENDING)
        self.order.update_status(OrderStatus.CONFIRMED)
        self.assertEqual(self.order.status, OrderStatus.CONFIRMED)
    
    def test_estimated_time(self):
        """Test estimated preparation time."""
        item1 = self.menu.add_item("Fast", "Desc", 5.0, Category.BEVERAGE, 5)
        item2 = self.menu.add_item("Slow", "Desc", 20.0, Category.MAIN_COURSE, 30)
        
        self.order.add_item(item1, 1)
        self.order.add_item(item2, 1)
        self.assertEqual(self.order.get_estimated_time(), 30)


class TestOrderManager(unittest.TestCase):
    """Test cases for OrderManager class."""
    
    def setUp(self):
        self.manager = OrderManager()
    
    def test_create_order(self):
        """Test creating a new order."""
        order = self.manager.create_order("Customer", table_number=1)
        self.assertIsNotNone(order)
        self.assertEqual(order.customer_name, "Customer")
    
    def test_get_order(self):
        """Test retrieving an order."""
        order = self.manager.create_order("Customer")
        retrieved = self.manager.get_order(order.id)
        self.assertEqual(retrieved.id, order.id)
    
    def test_cancel_order(self):
        """Test cancelling an order."""
        order = self.manager.create_order("Customer")
        self.assertTrue(self.manager.cancel_order(order.id))
        self.assertEqual(order.status, OrderStatus.CANCELLED)
    
    def test_get_active_orders(self):
        """Test getting active orders."""
        order1 = self.manager.create_order("Customer 1")
        order2 = self.manager.create_order("Customer 2")
        order3 = self.manager.create_order("Customer 3")
        order3.update_status(OrderStatus.COMPLETED)
        
        active = self.manager.get_active_orders()
        self.assertEqual(len(active), 2)


class TestOrderingSystem(unittest.TestCase):
    """Test cases for OrderingSystem class."""
    
    def setUp(self):
        self.system = OrderingSystem()
    
    def test_add_to_cart(self):
        """Test adding items to cart."""
        self.assertTrue(self.system.add_to_cart(1, 2))
        self.assertEqual(self.system.current_cart.get_item_count(), 2)
    
    def test_checkout(self):
        """Test checkout process."""
        self.system.add_to_cart(1, 1)
        order = self.system.checkout("Test Customer", 1)
        self.assertIsNotNone(order)
        self.assertEqual(len(order.items), 1)
        self.assertTrue(self.system.current_cart.is_empty())
    
    def test_checkout_empty_cart(self):
        """Test checkout with empty cart."""
        order = self.system.checkout("Customer")
        self.assertIsNone(order)
    
    def test_update_order_status(self):
        """Test updating order status through system."""
        self.system.add_to_cart(1, 1)
        order = self.system.checkout("Customer")
        self.assertTrue(self.system.update_order_status(order.id, OrderStatus.PREPARING))
        retrieved = self.system.get_order(order.id)
        self.assertEqual(retrieved.status, OrderStatus.PREPARING)


def run_tests():
    """Run all tests."""
    print("Running Smart Ordering System Tests...\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMenu))
    suite.addTests(loader.loadTestsFromTestCase(TestCart))
    suite.addTests(loader.loadTestsFromTestCase(TestOrder))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderManager))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderingSystem))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
