import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.utils.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships
    orders = relationship("Order", back_populates="user")

    def __init__(self, full_name, gender, age, email, is_verified, hashed_password):
        self.full_name = full_name
        self.gender = gender
        self.age = age
        self.email = email
        self.is_verified = is_verified
        self.hashed_password = hashed_password
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class Operator(Base):
    __tablename__ = "operator"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships
    restaurants = relationship("Restaurant", back_populates="owner")


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('operator.id'))
    description = Column(Text, nullable=False)
    avatar = Column(String, nullable=False)
    location = Column(String, nullable=False)
    views = Column(Integer, nullable=False)
    scans = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    owner = relationship("Operator", back_populates="restaurants")
    orders = relationship("Order", back_populates="restaurant")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    icon = Column(String, nullable=False)
    # Relationships
    menu_items = relationship("Meal", back_populates="category")


class Meal(Base):
    __tablename__ = "meal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    image_url = Column(String)

    # Relationships
    category = relationship("Category", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")


class OrderStatus(str, enum.Enum):
    PREPARING = "preparing"
    READY = "ready"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.PREPARING)
    table_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    meal_id = Column(Integer, ForeignKey("meal.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("Meal", back_populates="order_items")


class PaymentStatus(str, enum.Enum):
    WAITING = "waiting"
    PAID = "paid"
    CANCELLED = "cancelled"

class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.WAITING)
    total = Column(Integer, nullable=False)
    cash_payment = Column(Boolean, nullable=False)
    card_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)