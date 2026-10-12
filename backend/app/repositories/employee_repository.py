"""Employee repository (data access layer).

Responsible ONLY for talking to the database. No business or
validation logic lives here that belongs in the service layer.

This separation makes it easy to change the underlying persistence
(e.g., add caching, change ORM, or move to raw SQL) without touching
routers or business rules.
"""

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.employee import Employee


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        search: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[Employee], int]:
        """Return (rows, total_count) for matching employees.

        Searches employee names or departments using case-insensitive
        substring matching.

        Only the requested page is fetched from the database using
        LIMIT/OFFSET. The total count query uses COUNT(*) over the
        same filter rather than loading all rows into Python.
        This keeps the endpoint efficient as the table grows.
        """
        query = self.db.query(Employee)

        if search:
            term = f"%{search}%"

            query = query.filter(
                or_(
                    Employee.name.ilike(term),
                    Employee.department.ilike(term),
                )
            )

        total = query.with_entities(func.count(Employee.id)).scalar() or 0

        rows = query.order_by(Employee.name.asc()).limit(limit).offset(offset).all()

        return rows, total
