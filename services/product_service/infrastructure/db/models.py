from enum import StrEnum
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, Enum as SQLEnum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProductCategory(StrEnum):
    MOUNT = "mount"
    PET = "pet"
    SUBSCRIPTION = "subscription"
    SERVICE = "service"
    COSMETIC = "cosmetic"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    profile_picture_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(SQLEnum(ProductCategory), nullable=False)
    stock = Column(Integer, default=0)
    image_url = Column(String(255), nullable=True)