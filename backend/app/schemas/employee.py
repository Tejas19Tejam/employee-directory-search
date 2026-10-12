"""Pydantic schemas for request/response validation."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class EmployeeRead(BaseModel):
    """Shape of an employee returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    department: str
    designation: str
    date_of_joining: date


class EmployeeListResponse(BaseModel):
    """Paginated list response envelope."""

    items: list[EmployeeRead]
    total: int
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    """Consistent error payload shape across the API."""

    detail: str


# Reusable field constraints for query parameters, kept here so
# routers and services agree on the same validation rules.
SearchQuery = Field(
    default=None,
    min_length=1,
    max_length=100,
    description="Search term matched against employee name or department.",
)