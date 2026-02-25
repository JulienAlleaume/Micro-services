from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Style SQLAlchemy 2.0 : Mapped[T] + mapped_column()
# Pylance connaît le type exact de chaque colonne ET les opérateurs de
# comparaison (==, >, <…) produisent des expressions de colonne, pas des bool.
class Base(DeclarativeBase):
    pass


class PriceSchema(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    product_name: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(10), default="gold")
