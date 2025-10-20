"""Main ordering system that coordinates all components."""

from typing import Optional
from menu import Menu, MenuItem, Category
from order import Order, OrderManager, OrderStatus, OrderItem
from cart import Cart


class OrderingSystem:
    """Main smart ordering system for restaurants."""
    
    def __init__(self):
        self.menu = Menu()
        self.order_manager = OrderManager()
        self.current_cart = Cart()
        self._initialize_sample_menu()
    
    def _initialize_sample_menu(self):
        """Initialize the menu with sample items."""
        # Appetizers
        self.menu.add_item(
            "Caesar Salad",
            "Fresh romaine lettuce with parmesan cheese and croutons",
            8.99,
            Category.APPETIZER,
            10
        )
        self.menu.add_item(
            "Bruschetta",
            "Toasted bread topped with tomatoes, garlic, and basil",
            7.50,
            Category.APPETIZER,
            8
        )
        self.menu.add_item(
            "Chicken Wings",
            "Crispy wings with your choice of sauce",
            12.99,
            Category.APPETIZER,
            15
        )
        
        # Main Courses
        self.menu.add_item(
            "Grilled Salmon",
            "Fresh Atlantic salmon with herbs and lemon",
            24.99,
            Category.MAIN_COURSE,
            25
        )
        self.menu.add_item(
            "Ribeye Steak",
            "12oz premium ribeye cooked to your preference",
            32.99,
            Category.MAIN_COURSE,
            30
        )
        self.menu.add_item(
            "Pasta Carbonara",
            "Creamy pasta with bacon and parmesan",
            18.99,
            Category.MAIN_COURSE,
            20
        )
        self.menu.add_item(
            "Margherita Pizza",
            "Classic pizza with tomato, mozzarella, and basil",
            15.99,
            Category.MAIN_COURSE,
            18
        )
        
        # Desserts
        self.menu.add_item(
            "Tiramisu",
            "Italian coffee-flavored dessert",
            8.99,
            Category.DESSERT,
            5
        )
        self.menu.add_item(
            "Chocolate Lava Cake",
            "Warm chocolate cake with molten center",
            9.99,
            Category.DESSERT,
            12
        )
        
        # Beverages
        self.menu.add_item(
            "Soft Drink",
            "Coke, Sprite, or Fanta",
            2.99,
            Category.BEVERAGE,
            2
        )
        self.menu.add_item(
            "Fresh Juice",
            "Orange, Apple, or Cranberry",
            4.99,
            Category.BEVERAGE,
            3
        )
        self.menu.add_item(
            "Coffee",
            "Freshly brewed coffee",
            3.50,
            Category.BEVERAGE,
            3
        )
        
        # Side Dishes
        self.menu.add_item(
            "French Fries",
            "Crispy golden fries",
            4.99,
            Category.SIDE_DISH,
            10
        )
        self.menu.add_item(
            "Garlic Bread",
            "Toasted bread with garlic butter",
            5.50,
            Category.SIDE_DISH,
            8
        )
    
    def browse_menu(self, category: Optional[Category] = None) -> str:
        """Browse the menu, optionally filtered by category."""
        return self.menu.display_menu(category)
    
    def add_to_cart(self, item_id: int, quantity: int = 1, 
                    special_instructions: str = "") -> bool:
        """Add an item to the shopping cart."""
        item = self.menu.get_item(item_id)
        if item and item.available:
            self.current_cart.add_item(item, quantity, special_instructions)
            return True
        return False
    
    def remove_from_cart(self, item_id: int) -> bool:
        """Remove an item from the shopping cart."""
        return self.current_cart.remove_item(item_id)
    
    def view_cart(self) -> str:
        """View the current shopping cart."""
        return self.current_cart.display()
    
    def clear_cart(self):
        """Clear the shopping cart."""
        self.current_cart.clear()
    
    def checkout(self, customer_name: str, table_number: Optional[int] = None) -> Optional[Order]:
        """Checkout and create an order from the cart."""
        if self.current_cart.is_empty():
            return None
        
        order = self.order_manager.create_order(customer_name, table_number)
        
        # Transfer cart items to order
        for cart_item in self.current_cart.items:
            order.add_item(
                cart_item.menu_item,
                cart_item.quantity,
                cart_item.special_instructions
            )
        
        # Clear the cart
        self.current_cart.clear()
        
        return order
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """Get an order by ID."""
        return self.order_manager.get_order(order_id)
    
    def update_order_status(self, order_id: int, status: OrderStatus) -> bool:
        """Update the status of an order."""
        order = self.order_manager.get_order(order_id)
        if order:
            order.update_status(status)
            return True
        return False
    
    def cancel_order(self, order_id: int) -> bool:
        """Cancel an order."""
        return self.order_manager.cancel_order(order_id)
    
    def get_active_orders(self):
        """Get all active orders."""
        return self.order_manager.get_active_orders()
    
    def get_order_summary(self) -> str:
        """Get a summary of all active orders."""
        active_orders = self.get_active_orders()
        if not active_orders:
            return "\nNo active orders."
        
        output = ["\n=== Active Orders ==="]
        for order in sorted(active_orders, key=lambda x: x.id):
            output.append(f"\nOrder #{order.id} - {order.customer_name}")
            output.append(f"  Status: {order.status.value}")
            output.append(f"  Items: {len(order.items)}")
            output.append(f"  Total: ${order.get_total():.2f}")
        
        return "\n".join(output)
