"""Employee ORM model.

Indexing strategy (performance):

- Name and department each have a dedicated index so prefix searches
  and exact-match filtering can stay efficient as the table grows.
- A composite index is intentionally avoided because the API searches
  name OR department with the same term.
- Email is unique and indexed because it is a natural lookup key
  and must not collide between employees.
"""

from datetime import date

from sqlalchemy import Date, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Employee(Base):
    __tablename__ = "employees"

    __table_args__ = (
        Index("ix_employees_name", "name"),
        Index("ix_employees_department", "department"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    designation: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    date_of_joining: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )