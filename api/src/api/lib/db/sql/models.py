from sqlalchemy import DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

class Base(DeclarativeBase):
    pass


class Migrations(Base):
    __tablename__ = 'Migrations'

    name: Mapped[str] = mapped_column(Text, primary_key=True)
    hash: Mapped[str] = mapped_column(Text)
    applied_at: Mapped[datetime.datetime] = mapped_column(DateTime)


class Ping(Base):
    __tablename__ = 'ping'

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    data: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime)
