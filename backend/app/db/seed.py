"""Seed script that creates tables (if missing) and inserts sample employee data.

Run with:
    python -m app.db.seed
"""

from datetime import date

from sqlalchemy.orm import Session

from app.db.session import Base, SessionLocal, engine
from app.models.employee import Employee


SAMPLE_EMPLOYEES = [
    {
        "name": "Rahul Sharma",
        "email": "rahul.sharma@example.com",
        "department": "Engineering",
        "designation": "Software Engineer",
        "date_of_joining": date(2021, 3, 15),
    },
    {
        "name": "Rahul Verma",
        "email": "rahul.verma@example.com",
        "department": "Marketing",
        "designation": "Marketing Analyst",
        "date_of_joining": date(2020, 7, 1),
    },
    {
        "name": "Priya Nair",
        "email": "priya.nair@example.com",
        "department": "Engineering",
        "designation": "Senior Software Engineer",
        "date_of_joining": date(2019, 11, 20),
    },
    {
        "name": "Ananya Gupta",
        "email": "ananya.gupta@example.com",
        "department": "Human Resources",
        "designation": "HR Manager",
        "date_of_joining": date(2018, 5, 10),
    },
    {
        "name": "Vikram Singh",
        "email": "vikram.singh@example.com",
        "department": "Finance",
        "designation": "Financial Analyst",
        "date_of_joining": date(2022, 1, 5),
    },
    {
        "name": "Sneha Reddy",
        "email": "sneha.reddy@example.com",
        "department": "Engineering",
        "designation": "QA Engineer",
        "date_of_joining": date(2021, 9, 12),
    },
    {
        "name": "Arjun Mehta",
        "email": "arjun.mehta@example.com",
        "department": "Sales",
        "designation": "Sales Executive",
        "date_of_joining": date(2020, 2, 28),
    },
    {
        "name": "Kavya Iyer",
        "email": "kavya.iyer@example.com",
        "department": "Design",
        "designation": "UI/UX Designer",
        "date_of_joining": date(2023, 4, 18),
    },
    {
        "name": "Rohan Kapoor",
        "email": "rohan.kapoor@example.com",
        "department": "Engineering",
        "designation": "DevOps Engineer",
        "date_of_joining": date(2022, 8, 1),
    },
    {
        "name": "Ishita Joshi",
        "email": "ishita.joshi@example.com",
        "department": "Finance",
        "designation": "Accountant",
        "date_of_joining": date(2019, 6, 25),
    },
    {
        "name": "Karan Malhotra",
        "email": "karan.malhotra@example.com",
        "department": "Marketing",
        "designation": "Content Strategist",
        "date_of_joining": date(2021, 12, 3),
    },
    {
        "name": "Divya Pillai",
        "email": "divya.pillai@example.com",
        "department": "Human Resources",
        "designation": "Recruiter",
        "date_of_joining": date(2020, 10, 14),
    },
]


def seed() -> None:
    """Create database tables and insert sample employees if needed."""
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        existing = db.query(Employee).count()

        if existing > 0:
            print(
                f"Employees table already has {existing} rows. "
                "Skipping seed."
            )
            return

        db.bulk_insert_mappings(Employee, SAMPLE_EMPLOYEES)
        db.commit()

        print(f"Seeded {len(SAMPLE_EMPLOYEES)} employees.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()