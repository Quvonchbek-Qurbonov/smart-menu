"""Order management for the smart ordering system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
from menu import MenuItem


class OrderStatus(Enum):
    """Order status types."""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    READY = "Ready"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


@dataclass
class OrderItem:
    """Represents an item in an order."""
    menu_item: MenuItem
    quantity: int
    special_instructions: str = ""
    
    def get_subtotal(self) -> float:
        """Calculate subtotal for this order item."""
        return self.menu_item.price * self.quantity
    
    def __str__(self):
        base = f"{self.quantity}x {self.menu_item.name} - ${self.get_subtotal():.2f}"
        if self.special_instructions:
            base += f"\n   Note: {self.special_instructions}"
        return base


@dataclass
class Order:
    """Represents a customer order."""
    id: int
    customer_name: str
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    table_number: Optional[int] = None
    
    def add_item(self, menu_item: MenuItem, quantity: int = 1, 
                 special_instructions: str = "") -> OrderItem:
        """Add an item to the order."""
        # Check if item already exists in order
        for order_item in self.items:
            if order_item.menu_item.id == menu_item.id and \
               order_item.special_instructions == special_instructions:
                order_item.quantity += quantity
                return order_item
        
        # Add new item
        order_item = OrderItem(menu_item, quantity, special_instructions)
        self.items.append(order_item)
        return order_item
    
    def remove_item(self, menu_item_id: int) -> bool:
        """Remove an item from the order."""
        for i, order_item in enumerate(self.items):
            if order_item.menu_item.id == menu_item_id:
                self.items.pop(i)
                return True
        return False
    
    def get_total(self) -> float:
        """Calculate the total price of the order."""
        return sum(item.get_subtotal() for item in self.items)
    
    def get_estimated_time(self) -> int:
        """Estimate total preparation time in minutes."""
        if not self.items:
            return 0
        return max(item.menu_item.preparation_time for item in self.items)
    
    def update_status(self, status: OrderStatus):
        """Update the order status."""
        self.status = status
    
    def __str__(self):
        header = f"\nOrder #{self.id} - {self.customer_name}"
        if self.table_number:
            header += f" (Table {self.table_number})"
        header += f"\nStatus: {self.status.value}"
        header += f"\nCreated: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        
        if not self.items:
            return header + "\nNo items in order."
        
        items_str = "\n".join(f"  - {item}" for item in self.items)
        total = f"\nTotal: ${self.get_total():.2f}"
        est_time = f"\nEstimated Time: {self.get_estimated_time()} minutes"
        
        return header + "\n" + items_str + total + est_time


class OrderManager:
    """Manages all orders in the system."""
    
    def __init__(self):
        self.orders: Dict[int, Order] = {}
        self._next_id = 1000  # Start order numbers at 1000
    
    def create_order(self, customer_name: str, table_number: Optional[int] = None) -> Order:
        """Create a new order."""
        order = Order(
            id=self._next_id,
            customer_name=customer_name,
            table_number=table_number
        )
        self.orders[self._next_id] = order
        self._next_id += 1
        return order
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """Get an order by ID."""
        return self.orders.get(order_id)
    
    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """Get all orders with a specific status."""
        return [order for order in self.orders.values() if order.status == status]
    
    def get_active_orders(self) -> List[Order]:
        """Get all active orders (not completed or cancelled)."""
        active_statuses = {OrderStatus.PENDING, OrderStatus.CONFIRMED, 
                          OrderStatus.PREPARING, OrderStatus.READY}
        return [order for order in self.orders.values() if order.status in active_statuses]
    
    def cancel_order(self, order_id: int) -> bool:
        """Cancel an order."""
        order = self.get_order(order_id)
        if order and order.status not in {OrderStatus.COMPLETED, OrderStatus.CANCELLED}:
            order.update_status(OrderStatus.CANCELLED)
            return True
        return False
