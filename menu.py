"""Menu management for the smart ordering system."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class Category(Enum):
    """Menu item categories."""
    APPETIZER = "Appetizer"
    MAIN_COURSE = "Main Course"
    DESSERT = "Dessert"
    BEVERAGE = "Beverage"
    SIDE_DISH = "Side Dish"


@dataclass
class MenuItem:
    """Represents a menu item."""
    id: int
    name: str
    description: str
    price: float
    category: Category
    available: bool = True
    preparation_time: int = 15  # minutes
    
    def __str__(self):
        status = "✓" if self.available else "✗"
        return f"[{status}] {self.name} - ${self.price:.2f} ({self.preparation_time}min)"


class Menu:
    """Manages the restaurant menu."""
    
    def __init__(self):
        self.items: Dict[int, MenuItem] = {}
        self._next_id = 1
    
    def add_item(self, name: str, description: str, price: float, 
                 category: Category, preparation_time: int = 15) -> MenuItem:
        """Add a new item to the menu."""
        item = MenuItem(
            id=self._next_id,
            name=name,
            description=description,
            price=price,
            category=category,
            preparation_time=preparation_time
        )
        self.items[self._next_id] = item
        self._next_id += 1
        return item
    
    def get_item(self, item_id: int) -> Optional[MenuItem]:
        """Get a menu item by ID."""
        return self.items.get(item_id)
    
    def get_items_by_category(self, category: Category) -> List[MenuItem]:
        """Get all items in a specific category."""
        return [item for item in self.items.values() if item.category == category]
    
    def get_available_items(self) -> List[MenuItem]:
        """Get all available menu items."""
        return [item for item in self.items.values() if item.available]
    
    def set_availability(self, item_id: int, available: bool) -> bool:
        """Set the availability of a menu item."""
        item = self.get_item(item_id)
        if item:
            item.available = available
            return True
        return False
    
    def display_menu(self, category: Optional[Category] = None) -> str:
        """Display the menu, optionally filtered by category."""
        if category:
            items = self.get_items_by_category(category)
            title = f"\n{category.value}s"
        else:
            items = list(self.items.values())
            title = "\nFull Menu"
        
        if not items:
            return f"{title}\nNo items available."
        
        output = [title]
        output.append("=" * 50)
        for item in sorted(items, key=lambda x: x.id):
            output.append(f"ID: {item.id:2d} | {item}")
            output.append(f"        {item.description}")
        return "\n".join(output)
