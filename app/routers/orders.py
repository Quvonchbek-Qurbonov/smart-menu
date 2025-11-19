from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.database import get_db
from app.models.order import Order, OrderItem, OrderStatus
from app.models.menu import MenuItem
from app.models.user import User
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.utils.dependencies import get_current_user, get_staff_or_admin_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
        order_data: OrderCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Create a new order"""
    if not order_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )

    # Calculate total and validate items
    total_amount = 0.0
    order_items_to_create = []

    for item in order_data.items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with id {item.menu_item_id} not found"
            )

        if not menu_item.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item '{menu_item.name}' is not available"
            )

        item_total = menu_item.price * item.quantity
        total_amount += item_total

        order_items_to_create.append({
            "menu_item_id": item.menu_item_id,
            "quantity": item.quantity,
            "price": menu_item.price,
            "notes": item.notes
        })

    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        table_number=order_data.table_number,
        notes=order_data.notes,
        status=OrderStatus.PENDING
    )

    db.add(order)
    db.flush()  # Get order.id without committing

    # Create order items
    for item_data in order_items_to_create:
        order_item = OrderItem(order_id=order.id, **item_data)
        db.add(order_item)

    db.commit()
    db.refresh(order)

    return order


@router.get("", response_model=List[OrderResponse])
def get_orders(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        status: Optional[OrderStatus] = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get orders (users see their own, staff/admin see all)"""
    query = db.query(Order)

    # Regular customers can only see their own orders
    if current_user.role.value == "customer":
        query = query.filter(Order.user_id == current_user.id)

    if status:
        query = query.filter(Order.status == status)

    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
        order_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get a specific order by ID"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Check permissions: users can only see their own orders
    if current_user.role.value == "customer" and order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )

    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
        order_id: int,
        order_data: OrderUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_staff_or_admin_user)
):
    """Update an order (Staff/Admin only)"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Update fields
    update_data = order_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)

    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(
        order_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Cancel an order"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Check permissions: users can only cancel their own orders
    if current_user.role.value == "customer" and order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this order"
        )

    # Only pending or confirmed orders can be cancelled
    if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order cannot be cancelled at this stage"
        )

    order.status = OrderStatus.CANCELLED
    db.commit()

    return None