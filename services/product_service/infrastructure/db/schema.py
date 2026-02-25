from typing import Optional
from sqlalchemy import String, Integer, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from domain.entities import ProductCategory


class Base(DeclarativeBase):
    pass


class ProductShema(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    category: Mapped[str] = mapped_column(SQLEnum(ProductCategory))
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
