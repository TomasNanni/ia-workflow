import os
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL environment variable not set.")
    exit(1)

# Fix for potential postgres:// vs postgresql:// issue
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- Models ---

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    city = Column(String(50))
    country = Column(String(50))

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer")
    product = relationship("Product")

# --- Seeding Logic ---

def seed_data():
    print("Creating tables...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    db = SessionLocal()
    try:
        print("Seeding customers...")
        customers = [
            Customer(name=f"Customer {i}", email=f"user{i}@example.com", city=random.choice(["Buenos Aires", "Madrid", "New York", "Berlin", "Beijing", "London", "Paris", "Tokyo", "Rome", "Sydney"]), country=random.choice(["Argentina", "España", "USA", "Alemania", "China", "UK", "Francia", "Japón", "Italia", "Australia"]))
            for i in range(1, 21)
        ]
        db.add_all(customers)
        db.commit()

        print("Seeding products...")
        product_names = [
            "Laptop Pro 15", "Smartphone X", "Wireless Headphones", "Coffee Maker", "Mechanical Keyboard",
            "Monitor 4K", "External SSD 1TB", "Webcam HD", "Desk Lamp", "Ergonomic Chair",
            "Gaming Mouse", "USB-C Hub", "Tablet Air", "Smart Watch", "Bluetooth Speaker",
            "Router Wi-Fi 6", "Power Bank 20k", "Microphone Yeti", "Graphic Tablet", "VR Headset"
        ]
        categories = ["Electronics", "Audio", "Home", "Accessories", "Furniture"]
        
        products = [
            Product(name=name, category=random.choice(categories), price=round(random.uniform(20.0, 1500.0), 2), stock=random.randint(10, 100))
            for name in product_names
        ]
        db.add_all(products)
        db.commit()

        print("Seeding sales...")
        # Get committed objects to have IDs
        db_customers = db.query(Customer).all()
        db_products = db.query(Product).all()

        sales = []
        start_date = datetime.utcnow() - timedelta(days=90)

        for _ in range(100):
            customer = random.choice(db_customers)
            product = random.choice(db_products)
            qty = random.randint(1, 3)
            sale_date = start_date + timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))
            
            sales.append(Sale(
                customer_id=customer.id,
                product_id=product.id,
                quantity=qty,
                total_price=product.price * qty,
                sale_date=sale_date
            ))
        
        db.add_all(sales)
        db.commit()
        print("Success: Database seeded with sample E-commerce data!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
