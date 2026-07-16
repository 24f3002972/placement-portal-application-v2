from backend.app import app
from backend.models import db
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

# run like this from backend folder
# python3 -m scripts.init_db

with app.app_context():
     # delete all data
    db.create_all() # create fresh tables
    datastore : SQLAlchemyUserDatastore = app.datastore

    admin_role = datastore.find_or_create_role("admin", description = "super user")
    manager_role = datastore.find_or_create_role("company", description = "conduct placement drives")
    customer_role = datastore.find_or_create_role("student", description = "apply for placements")

    if not datastore.find_user(email = "admin@study"):
        datastore.create_user(
            email = "admin@study",
            name = "admin_01",
            password = hash_password('pass'),
        )
    if not datastore.find_user(email = "company@study"):
        datastore.create_user(
            email = "company@study",
            name = "company_01",
            password = hash_password('pass'),
        )
    if not datastore.find_user(email = "student@study"):
        datastore.create_user(
            email = "student@study",
            name = "student_01",
            password = hash_password('pass'),
        )


    try:
        db.session.commit()
        print("✅ created successfully")
    except:
        db.session.rollback()
        print("Error while creating")

    admin01 = datastore.find_user(email="admin@study")
    company01 = datastore.find_user(email="company@study")
    student = datastore.find_user(email="student@study")

    admin_role = datastore.find_role("admin")
    company_role = datastore.find_role("company")
    student_role = datastore.find_role("student")

    datastore.add_role_to_user(admin01, admin_role)
    datastore.add_role_to_user(company01, company_role)
    datastore.add_role_to_user(student, student_role)

    try:
        db.session.commit()
        print("✅ Added roles")
    except:
        db.session.rollback()
        print("error adding roles")
