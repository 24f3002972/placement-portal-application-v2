from .extensions import db
from datetime import datetime, timezone
from flask_security.core import UserMixin, RoleMixin

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime(), default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(), default = lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class User(BaseModel, UserMixin):
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique=True)
    password = db.Column(db.String, nullable = False)
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, default = True) # if Active = False, then the user will not be able to login
    company = db.relationship("Company", back_populates="user", uselist=False)
    student = db.relationship("Student", back_populates="user", uselist=False)
    roles = db.relationship("Role", secondary='roles_users', backref="users")
    requests = db.relationship("Request", back_populates='user')

class Role(BaseModel, RoleMixin):
    name = db.Column(db.String, unique=True, nullable=False) #admin, company, student
    description = db.Column(db.String, nullable=False)
    roles_users = db.Table("roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")))


class Company(BaseModel):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    hr_contact = db.Column(db.String, unique=True)
    website = db.Column(db.String, unique=True)
    user = db.relationship("User", back_populates="company")
    drive = db.relationship("Drive", back_populates="company")

class Student(BaseModel):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    branch = db.Column(db.String, nullable=False)
    cgpa = db.Column(db.Numeric(10, 2), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", back_populates="student")
    application = db.relationship("Application", back_populates="student")

class Request(BaseModel):
    data = db.Column(db.JSON)
    status = db.Column(db.Enum("created", "approved", "rejected"), default="created", nullable=False)
    request_type = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', back_populates='requests')

class Drive(BaseModel):
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    job_title = db.Column(db.String, nullable=False)
    job_description = db.Column(db.String)
    eligible_branch = db.Column(db.String, nullable=False)
    minimum_cgpa = db.Column(db.Numeric(3,2), nullable=False)
    eligible_year = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.Enum("Approved", "Rejected", "Pending", "Closed"), default="Pending")
    application = db.relationship("Application", back_populates="drive")
    company = db.relationship("Company", back_populates="drive")

class Application(BaseModel):
    __table_args__ = (db.UniqueConstraint("student_id", "drive_id"),)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("drive.id"), nullable=False)
    date = db.Column(db.DateTime(),default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.Enum("Applied", "Shortlisted", "Selected", "Rejected"), default="Applied")
    drive = db.relationship("Drive", back_populates="application")
    student = db.relationship("Student", back_populates="application")



