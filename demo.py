#!/usr/bin/env python3
"""Demonstration script for the smart ordering system."""

from ordering_system import OrderingSystem
from menu import Category
from order import OrderStatus


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_menu_browsing(system):
    """Demonstrate menu browsing."""
    print_section("1. Menu Browsing")
    
    print("\n>>> Browsing full menu:")
    print(system.browse_menu())
    
    print("\n>>> Browsing appetizers only:")
    print(system.browse_menu(Category.APPETIZER))


def demo_cart_operations(system):
    """Demonstrate cart operations."""
    print_section("2. Shopping Cart Operations")
    
    print("\n>>> Adding items to cart:")
    system.add_to_cart(1, 2)  # 2x Caesar Salad
    print("Added 2x Caesar Salad")
    
    system.add_to_cart(5, 1, "Medium rare, no salt")  # Ribeye Steak
    print("Added 1x Ribeye Steak (Medium rare, no salt)")
    
    system.add_to_cart(11, 2)  # 2x Soft Drink
    print("Added 2x Soft Drink")
    
    system.add_to_cart(14, 1)  # French Fries
    print("Added 1x French Fries")
    
    print("\n>>> Viewing cart:")
    print(system.view_cart())
    
    print("\n>>> Removing an item from cart:")
    system.remove_from_cart(14)  # Remove French Fries
    print("Removed French Fries")
    print(system.view_cart())


def demo_checkout(system):
    """Demonstrate checkout process."""
    print_section("3. Checkout Process")
    
    print("\n>>> Creating order:")
    order = system.checkout("John Doe", table_number=5)
    if order:
        print(order)
        return order.id
    return None


def demo_order_management(system, order_id):
    """Demonstrate order management."""
    print_section("4. Order Management")
    
    print("\n>>> Viewing order:")
    order = system.get_order(order_id)
    if order:
        print(order)
    
    print("\n>>> Updating order status to CONFIRMED:")
    system.update_order_status(order_id, OrderStatus.CONFIRMED)
    order = system.get_order(order_id)
    print(f"Order status: {order.status.value}")
    
    print("\n>>> Updating order status to PREPARING:")
    system.update_order_status(order_id, OrderStatus.PREPARING)
    order = system.get_order(order_id)
    print(f"Order status: {order.status.value}")
    
    print("\n>>> Updating order status to READY:")
    system.update_order_status(order_id, OrderStatus.READY)
    order = system.get_order(order_id)
    print(f"Order status: {order.status.value}")


def demo_multiple_orders(system):
    """Demonstrate handling multiple orders."""
    print_section("5. Multiple Orders Management")
    
    # Create second order
    print("\n>>> Creating second order:")
    system.add_to_cart(4, 1)  # Grilled Salmon
    system.add_to_cart(8, 1)  # Tiramisu
    system.add_to_cart(12, 1)  # Fresh Juice
    order2 = system.checkout("Jane Smith", table_number=3)
    if order2:
        print(f"Order #{order2.id} created for Jane Smith")
    
    # Create third order
    print("\n>>> Creating third order:")
    system.add_to_cart(7, 2)  # 2x Margherita Pizza
    system.add_to_cart(11, 4)  # 4x Soft Drink
    order3 = system.checkout("Bob Johnson", table_number=7)
    if order3:
        print(f"Order #{order3.id} created for Bob Johnson")
    
    # View all active orders
    print("\n>>> Viewing all active orders:")
    print(system.get_order_summary())


def demo_advanced_features(system):
    """Demonstrate advanced features."""
    print_section("6. Advanced Features")
    
    print("\n>>> Setting menu item availability:")
    system.menu.set_availability(5, False)  # Make Ribeye unavailable
    print("Ribeye Steak is now unavailable")
    
    print("\n>>> Attempting to add unavailable item:")
    if not system.add_to_cart(5, 1):
        print("✗ Could not add Ribeye Steak (unavailable)")
    
    print("\n>>> Getting available items only:")
    available = system.menu.get_available_items()
    print(f"Total available items: {len(available)}")
    
    # Restore availability
    system.menu.set_availability(5, True)
    
    print("\n>>> Creating order with special instructions:")
    system.add_to_cart(6, 1, "Extra cheese, no bacon")  # Pasta Carbonara
    system.add_to_cart(13, 1, "Extra hot")  # Coffee
    order = system.checkout("Alice Brown", table_number=2)
    if order:
        print(order)


def main():
    """Run the complete demonstration."""
    print("=" * 70)
    print("  SMART ORDERING SYSTEM - DEMONSTRATION")
    print("  A comprehensive restaurant ordering solution")
    print("=" * 70)
    
    system = OrderingSystem()
    
    # Run demonstrations
    demo_menu_browsing(system)
    demo_cart_operations(system)
    order_id = demo_checkout(system)
    
    if order_id:
        demo_order_management(system, order_id)
    
    demo_multiple_orders(system)
    demo_advanced_features(system)
    
    print_section("Demo Complete!")
    print("\nThe smart ordering system successfully demonstrated:")
    print("✓ Menu browsing and categorization")
    print("✓ Shopping cart management")
    print("✓ Order creation and checkout")
    print("✓ Order status tracking")
    print("✓ Multiple order handling")
    print("✓ Special instructions support")
    print("✓ Menu item availability management")
    print("\nThank you for exploring the Smart Ordering System!")


if __name__ == "__main__":
    main()
