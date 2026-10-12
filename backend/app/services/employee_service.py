"""Employee service (business logic layer).

Routers call into this layer instead of touching the repository
or ORM directly. This is where business rules live (e.g.,
trimming/normalizing search terms and enforcing pagination bounds)
so they stay independent of the HTTP transport and are easy to
unit test or reuse (e.g., from a CLI or background job).
"""

from sqlalchemy.exc import OperationalError

from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeListResponse, EmployeeRead

MAX_LIMIT = 100
DEFAULT_LIMIT = 20


class EmployeeServiceError(Exception):
    """Base exception for service-level errors, caught by the router."""


class InvalidSearchError(EmployeeServiceError):
    """Raised when the caller-supplied search/pagination params are invalid."""


class DatabaseUnavailableError(EmployeeServiceError):
    """Raised when the database cannot be reached."""


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def search_employees(
        self,
        search: str | None,
        limit: int,
        offset: int,
    ) -> EmployeeListResponse:
        normalized_search = self._normalize_search(search)
        self._validate_pagination(limit, offset)

        try:
            rows, total = self.repository.search(
                normalized_search,
                limit,
                offset,
            )
        except OperationalError as exc:
            # Raised by SQLAlchemy when the database is unreachable
            # (connection refused, timeout, or connection-level failure).
            raise DatabaseUnavailableError(
                "Unable to reach the database. Please try again later."
            ) from exc

        return EmployeeListResponse(
            items=[
                EmployeeRead.model_validate(row)
                for row in rows
            ],
            total=total,
            limit=limit,
            offset=offset,
        )

    @staticmethod
    def _normalize_search(search: str | None) -> str | None:
        if search is None:
            return None

        trimmed = search.strip()

        if not trimmed:
            # Empty/whitespace-only search queries are treated as
            # validation errors rather than silently returning everything.
            # This keeps the caller's intent explicit.
            raise InvalidSearchError(
                "Search query cannot be empty or whitespace only."
            )

        return trimmed

    @staticmethod
    def _validate_pagination(limit: int, offset: int) -> None:
        if limit < 1 or limit > MAX_LIMIT:
            raise InvalidSearchError(
                f"'limit' must be between 1 and {MAX_LIMIT}."
            )

        if offset < 0:
            raise InvalidSearchError(
                "'offset' must be greater than or equal to 0."
            )