from sqlalchemy import Column, Integer, String, Boolean, Text, Enum as SQLEnum
from enum import StrEnum
from sqlalchemy.orm import declarative_base
from domain.models import ProductCategory

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    profile_picture_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

class ProductShema(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(ProductCategory), nullable=False)
    image_url = Column(String(255), nullable=True)
    