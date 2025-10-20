# Smart Menu - Restaurant Ordering System

A comprehensive smart ordering system for restaurants that streamlines the ordering process, manages menus, tracks orders, and enhances customer experience.

## Features

### Core Functionality
- **Menu Management**: Organize menu items by categories (Appetizers, Main Courses, Desserts, Beverages, Side Dishes)
- **Shopping Cart**: Add, remove, and modify items before placing an order
- **Order Processing**: Create, track, and manage customer orders with multiple status levels
- **Order Tracking**: Monitor order status from pending to completion
- **Special Instructions**: Add custom instructions for each menu item
- **Table Management**: Associate orders with table numbers
- **Availability Control**: Mark items as available or unavailable
- **Estimated Time**: Calculate preparation time for orders

### Technical Features
- Object-oriented design with clean separation of concerns
- Type hints for better code quality
- Dataclasses for clean data models
- Enum-based status and category management
- Comprehensive test coverage

## Installation

### Requirements
- Python 3.7 or higher

### Setup
1. Clone the repository:
```bash
git clone https://github.com/Quvonchbek-Qurbonov/smart-menu.git
cd smart-menu
```

2. No additional dependencies required - uses only Python standard library!

## Usage

### Quick Start - Demo
Run the demonstration to see all features in action:
```bash
python3 demo.py
```

### Interactive CLI
Launch the interactive command-line interface:
```bash
python3 main.py
```

The CLI provides the following options:
1. Browse Full Menu
2. Browse by Category
3. Add Item to Cart
4. View Cart
5. Remove Item from Cart
6. Checkout
7. View Order
8. Update Order Status (Staff)
9. View Active Orders (Staff)
0. Exit

### Programmatic Usage

```python
from ordering_system import OrderingSystem
from menu import Category
from order import OrderStatus

# Initialize the system
system = OrderingSystem()

# Browse menu
print(system.browse_menu())
print(system.browse_menu(Category.APPETIZER))

# Add items to cart
system.add_to_cart(item_id=1, quantity=2)
system.add_to_cart(item_id=5, quantity=1, special_instructions="Medium rare")

# View cart
print(system.view_cart())

# Checkout
order = system.checkout(customer_name="John Doe", table_number=5)
print(order)

# Update order status
system.update_order_status(order.id, OrderStatus.PREPARING)

# View active orders
print(system.get_order_summary())
```

## Project Structure

```
smart-menu/
├── menu.py                     # Menu and MenuItem classes
├── order.py                    # Order management classes
├── cart.py                     # Shopping cart functionality
├── ordering_system.py          # Main system coordinator
├── main.py                     # Interactive CLI
├── demo.py                     # Demonstration script
├── test_ordering_system.py     # Test suite
└── README.md                   # This file
```

## Components

### Menu System (`menu.py`)
- **MenuItem**: Represents a single menu item with price, description, category
- **Menu**: Manages all menu items, categories, and availability
- **Category**: Enum for menu categories

### Cart System (`cart.py`)
- **CartItem**: Represents an item in the shopping cart
- **Cart**: Manages cart operations (add, remove, update, clear)

### Order System (`order.py`)
- **OrderItem**: Represents an item in an order
- **Order**: Manages individual orders with status tracking
- **OrderManager**: Coordinates multiple orders
- **OrderStatus**: Enum for order lifecycle states

### Main System (`ordering_system.py`)
- **OrderingSystem**: Main coordinator that integrates all components

## Running Tests

Execute the test suite to verify functionality:
```bash
python3 test_ordering_system.py
```

The test suite includes:
- Menu management tests
- Cart operation tests
- Order processing tests
- Order manager tests
- System integration tests

## Example Workflow

### Customer Workflow
1. Browse the menu by category or view all items
2. Add desired items to cart with quantities and special instructions
3. Review cart contents
4. Checkout with name and table number
5. Receive order confirmation with order ID and estimated time

### Staff Workflow
1. View active orders
2. Update order status as food is prepared:
   - PENDING → CONFIRMED → PREPARING → READY → COMPLETED
3. Monitor order queue
4. Cancel orders if needed

## Menu Categories

The system supports the following categories:
- **APPETIZER**: Starters and small plates
- **MAIN_COURSE**: Primary dishes
- **DESSERT**: Sweet treats
- **BEVERAGE**: Drinks
- **SIDE_DISH**: Accompaniments

## Order Status Flow

Orders progress through these statuses:
1. **PENDING**: Order created, awaiting confirmation
2. **CONFIRMED**: Order confirmed, ready to prepare
3. **PREPARING**: Food is being prepared
4. **READY**: Order is ready for pickup/serving
5. **COMPLETED**: Order has been delivered
6. **CANCELLED**: Order was cancelled

## Sample Menu

The system comes with a sample menu including:
- Appetizers: Caesar Salad, Bruschetta, Chicken Wings
- Main Courses: Grilled Salmon, Ribeye Steak, Pasta Carbonara, Margherita Pizza
- Desserts: Tiramisu, Chocolate Lava Cake
- Beverages: Soft Drinks, Fresh Juice, Coffee
- Side Dishes: French Fries, Garlic Bread

## Future Enhancements

Potential areas for expansion:
- Web interface with REST API
- Database integration for persistence
- Payment processing
- Kitchen display system
- Analytics and reporting
- Multi-language support
- Loyalty program integration
- Reservation system

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Author

Quvonchbek Qurbonov

## Acknowledgments

Built with Python using best practices for clean, maintainable code.