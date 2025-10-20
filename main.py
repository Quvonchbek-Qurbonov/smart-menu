#!/usr/bin/env python3
"""Command-line interface for the smart ordering system."""

import sys
from ordering_system import OrderingSystem
from menu import Category
from order import OrderStatus


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_menu():
    """Print the main menu options."""
    print("\n--- Smart Ordering System ---")
    print("1. Browse Full Menu")
    print("2. Browse by Category")
    print("3. Add Item to Cart")
    print("4. View Cart")
    print("5. Remove Item from Cart")
    print("6. Checkout")
    print("7. View Order")
    print("8. Update Order Status (Staff)")
    print("9. View Active Orders (Staff)")
    print("0. Exit")


def browse_by_category(system):
    """Browse menu by category."""
    print("\nCategories:")
    categories = list(Category)
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat.value}")
    
    try:
        choice = int(input("\nSelect category (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(categories):
            print(system.browse_menu(categories[choice - 1]))
        else:
            print("Invalid category selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def add_item_to_cart(system):
    """Add an item to the cart."""
    try:
        item_id = int(input("Enter item ID: "))
        quantity = int(input("Enter quantity (default 1): ") or "1")
        special_instructions = input("Any special instructions? (press Enter to skip): ").strip()
        
        if system.add_to_cart(item_id, quantity, special_instructions):
            print(f"✓ Added {quantity}x item #{item_id} to cart")
        else:
            print("✗ Could not add item. Check if item ID is valid and available.")
    except ValueError:
        print("Invalid input. Please enter valid numbers.")


def remove_from_cart(system):
    """Remove an item from the cart."""
    print(system.view_cart())
    try:
        item_id = int(input("\nEnter item ID to remove: "))
        if system.remove_from_cart(item_id):
            print(f"✓ Removed item #{item_id} from cart")
        else:
            print("✗ Item not found in cart.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def checkout(system):
    """Checkout and create an order."""
    cart_display = system.view_cart()
    print(cart_display)
    
    if system.current_cart.is_empty():
        return
    
    customer_name = input("\nEnter your name: ").strip()
    if not customer_name:
        print("Name is required for checkout.")
        return
    
    table_input = input("Enter table number (press Enter to skip): ").strip()
    table_number = int(table_input) if table_input else None
    
    order = system.checkout(customer_name, table_number)
    if order:
        print_header("Order Confirmed!")
        print(order)
        print("\nThank you for your order!")
    else:
        print("✗ Could not create order.")


def view_order(system):
    """View an order by ID."""
    try:
        order_id = int(input("Enter order ID: "))
        order = system.get_order(order_id)
        if order:
            print(order)
        else:
            print(f"✗ Order #{order_id} not found.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def update_order_status(system):
    """Update the status of an order."""
    try:
        order_id = int(input("Enter order ID: "))
        order = system.get_order(order_id)
        if not order:
            print(f"✗ Order #{order_id} not found.")
            return
        
        print(f"\nCurrent status: {order.status.value}")
        print("\nAvailable statuses:")
        statuses = list(OrderStatus)
        for i, status in enumerate(statuses, 1):
            print(f"{i}. {status.value}")
        
        choice = int(input("\nSelect new status: "))
        if 1 <= choice <= len(statuses):
            new_status = statuses[choice - 1]
            if system.update_order_status(order_id, new_status):
                print(f"✓ Order #{order_id} status updated to {new_status.value}")
            else:
                print("✗ Could not update order status.")
        else:
            print("Invalid status selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def main():
    """Main function to run the ordering system CLI."""
    print_header("Welcome to the Smart Ordering System")
    print("A modern restaurant ordering solution")
    
    system = OrderingSystem()
    
    while True:
        print_menu()
        try:
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                print(system.browse_menu())
            elif choice == "2":
                browse_by_category(system)
            elif choice == "3":
                add_item_to_cart(system)
            elif choice == "4":
                print(system.view_cart())
            elif choice == "5":
                remove_from_cart(system)
            elif choice == "6":
                checkout(system)
            elif choice == "7":
                view_order(system)
            elif choice == "8":
                update_order_status(system)
            elif choice == "9":
                print(system.get_order_summary())
            elif choice == "0":
                print("\nThank you for using Smart Ordering System!")
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n✗ An error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
