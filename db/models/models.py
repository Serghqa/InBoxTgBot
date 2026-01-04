from datetime import date as dt
from sqlalchemy import BigInteger, Date, ForeignKey, Integer,  String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Any


class Base(DeclarativeBase):

    pass


class User(Base):

    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True,)
    name: Mapped[str] = mapped_column(String)
