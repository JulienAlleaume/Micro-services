import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# En dev local : SQLite. En Docker (via docker-compose) : PostgreSQL via DATABASE_URL.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wow_shop.db")

# connect_args spécifique à SQLite (check_same_thread) ; ignoré pour PostgreSQL
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
