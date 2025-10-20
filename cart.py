"""Shopping cart functionality for the smart ordering system."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from menu import MenuItem


@dataclass
class CartItem:
    """Represents an item in the shopping cart."""
    menu_item: MenuItem
    quantity: int
    special_instructions: str = ""
    
    def get_subtotal(self) -> float:
        """Calculate subtotal for this cart item."""
        return self.menu_item.price * self.quantity


class Cart:
    """Shopping cart for building an order before submission."""
    
    def __init__(self):
        self.items: List[CartItem] = []
    
    def add_item(self, menu_item: MenuItem, quantity: int = 1, 
                 special_instructions: str = "") -> CartItem:
        """Add an item to the cart."""
        # Check if item already exists in cart
        for cart_item in self.items:
            if cart_item.menu_item.id == menu_item.id and \
               cart_item.special_instructions == special_instructions:
                cart_item.quantity += quantity
                return cart_item
        
        # Add new item
        cart_item = CartItem(menu_item, quantity, special_instructions)
        self.items.append(cart_item)
        return cart_item
    
    def remove_item(self, menu_item_id: int) -> bool:
        """Remove an item from the cart."""
        for i, cart_item in enumerate(self.items):
            if cart_item.menu_item.id == menu_item_id:
                self.items.pop(i)
                return True
        return False
    
    def update_quantity(self, menu_item_id: int, quantity: int) -> bool:
        """Update the quantity of an item in the cart."""
        if quantity <= 0:
            return self.remove_item(menu_item_id)
        
        for cart_item in self.items:
            if cart_item.menu_item.id == menu_item_id:
                cart_item.quantity = quantity
                return True
        return False
    
    def clear(self):
        """Clear all items from the cart."""
        self.items.clear()
    
    def get_total(self) -> float:
        """Calculate the total price of items in the cart."""
        return sum(item.get_subtotal() for item in self.items)
    
    def get_item_count(self) -> int:
        """Get the total number of items in the cart."""
        return sum(item.quantity for item in self.items)
    
    def is_empty(self) -> bool:
        """Check if the cart is empty."""
        return len(self.items) == 0
    
    def display(self) -> str:
        """Display the cart contents."""
        if self.is_empty():
            return "\nYour cart is empty."
        
        output = ["\n=== Shopping Cart ==="]
        for i, item in enumerate(self.items, 1):
            output.append(f"{i}. {item.quantity}x {item.menu_item.name} - ${item.get_subtotal():.2f}")
            if item.special_instructions:
                output.append(f"   Note: {item.special_instructions}")
        
        output.append("-" * 30)
        output.append(f"Total Items: {self.get_item_count()}")
        output.append(f"Total Price: ${self.get_total():.2f}")
        
        return "\n".join(output)
