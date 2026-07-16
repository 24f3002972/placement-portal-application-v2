import random
import uuid
from datetime import datetime, timedelta
from flask_security.utils import verify_password, hash_password
from faker import Faker
from faker_food import FoodProvider

from ..models import db, User, Role, Company, Student, Drive, Application
# change yourapp.models based on your project structure

fake = Faker()
fake.add_provider(FoodProvider)


def random_past_date(days=180):
    return datetime.now() - timedelta(days=random.randint(1, days))


def seed_data():
    print("Seeding started...")

    #Clear old data
    Application.query.delete()
    Drive.query.delete()
    Company.query.delete()
    Student.query.delete()
    User.query.delete()
    Role.query.delete()

    db.session.commit()

    # --------------------------
    # Create roles
    # --------------------------
    roles_data = {
    "admin": "System administrator",
    "company": "Recruiting company",
    "student": "Student user"
    }

    for role_name, desc in roles_data.items():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            db.session.add(Role(name=role_name, description=desc))

    db.session.commit()

    admin_role = Role.query.filter_by(name="admin").first()
    company_role = Role.query.filter_by(name="company").first()
    student_role = Role.query.filter_by(name="student").first()

    # --------------------------
    # Create admin
    # --------------------------
    admin_user = User(
        name="Main Admin",
        email="admin@example.com",
        password=hash_password("pass"),
        fs_uniquifier=str(uuid.uuid4()),
        active=True,
        created_at=random_past_date(200),
        roles=[admin_role]
    )

    db.session.add(admin_user)
    db.session.commit()

    companies = []
    students = []
    drives = []

    # --------------------------
    # Create 10 companies
    # --------------------------
    for i in range(10):
        company_created = random_past_date(150)

        user = User(
            name=fake.company(),
            email=f"company{i}@mail.com",
            password=hash_password("pass"),
            fs_uniquifier=str(uuid.uuid4()),
            active=True,
            created_at=company_created,
            roles=[company_role]
        )

        db.session.add(user)
        db.session.flush()

        company = Company(
            id=user.id,
            company_name=user.name,
            hr_contact=fake.phone_number(),
            website=fake.url(),
            created_at=company_created
        )

        db.session.add(company)
        companies.append(company)

    db.session.commit()

    # --------------------------
    # Create 50 students
    # --------------------------
    branches = ["CSE", "ECE", "ME", "CE", "EEE", "DS"]

    for i in range(50):
        student_created = random_past_date(120)

        user = User(
            name=fake.name(),
            email=f"student{i}@mail.com",
            password=hash_password("pass"),
            fs_uniquifier=str(uuid.uuid4()),
            active=True,
            created_at=student_created,
            roles=[student_role]
        )

        db.session.add(user)
        db.session.flush()

        student = Student(
            id=user.id,
            branch=random.choice(branches),
            cgpa=round(random.uniform(6.0, 9.9), 2),
            year=random.randint(1, 4),
            created_at=student_created
        )

        db.session.add(student)
        students.append(student)

    db.session.commit()

    # --------------------------
    # Create drives for companies
    # --------------------------
    job_titles = [
        "Software Engineer",
        "Data Analyst",
        "Backend Developer",
        "ML Engineer",
        "Cloud Engineer"
    ]

    for company in companies:
        for _ in range(random.randint(2, 5)):
            drive_created = random_past_date(90)

            drive = Drive(
                company_id=company.id,
                job_title=random.choice(job_titles),
                job_description=fake.text(max_nb_chars=200),
                eligible_branch=random.choice(["CSE", "IT", "ECE", "EEE", "ME", "CE"]),
                minimum_cgpa=round(random.uniform(6.0, 9.5), 2),
                eligible_year=random.choice([2, 3, 4]),
                deadline=(datetime.now() + timedelta(days=random.randint(10, 60))).date(),
                status=random.choice(
                    ["Approved", "Rejected", "Pending", "Closed"]
                ),
                created_at=drive_created
            )

            db.session.add(drive)
            drives.append(drive)

    db.session.commit()

    # --------------------------
    # Create applications
    # --------------------------
    for student in students:
        selected_drives = random.sample(
            drives,
            random.randint(1, min(5, len(drives)))
        )

        for drive in selected_drives:
            applied_date = random_past_date(60)

            application = Application(
                student_id=student.id,
                drive_id=drive.id,
                date=applied_date.date(),
                status=random.choice(
                    ["Applied", "Shortlisted", "Selected", "Rejected"]
                ),
                created_at=applied_date
            )

            db.session.add(application)

    db.session.commit()

    print("Seeding completed successfully!")


if __name__ == "__main__":
    from backend.app import app   # import your flask app

    with app.app_context():
        seed_data()