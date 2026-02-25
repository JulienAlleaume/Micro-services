from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Enum as SQLEnum
from datetime import datetime
from enum import StrEnum
from sqlalchemy.orm import declarative_base
from domain.entities import ProductCategory

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

class EventDB(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    aggregate_id = Column(Integer, index=True) # L'ID de l'objet concerné (ex: ID du produit)
    event_type = Column(String(100), nullable=False) # Le nom de l'événement (ex: ProductCreatedEvent)
    payload = Column(Text, nullable=False) # Les données JSON de l'événement
    created_at = Column(DateTime, default=datetime.utcnow)
