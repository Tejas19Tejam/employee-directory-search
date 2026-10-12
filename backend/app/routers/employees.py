"""Employee routes.

Routers are intentionally thin: they only handle HTTP concerns
(status codes, dependency wiring) and delegate all business logic
to the service layer. This keeps route handlers easy to read and
allows business logic to be reused or tested without spinning
up HTTP.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeListResponse
from app.services.employee_service import (
    DEFAULT_LIMIT,
    MAX_LIMIT,
    DatabaseUnavailableError,
    EmployeeService,
    InvalidSearchError,
)

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


def get_employee_service(
    db: Session = Depends(get_db),
) -> EmployeeService:
    return EmployeeService(EmployeeRepository(db))


@router.get(
    "/",
    response_model=EmployeeListResponse,
    summary="Search employees by name or department",
)
def search_employees(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
        description="Term matched against employee name or department.",
    ),
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=1,
        le=MAX_LIMIT,
        description="Page size.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of records to skip.",
    ),
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeListResponse:
    try:
        return service.search_employees(
            search=search,
            limit=limit,
            offset=offset,
        )

    except InvalidSearchError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except DatabaseUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc