from flask_restful import fields

user_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "active": fields.Boolean
}

company_fields = {
    "id": fields.Integer,
    "company_name": fields.String,
    "website": fields.String,
    "hr_contact": fields.String,
    "user": fields.Nested(user_fields)
}

student_fields = {
    "id": fields.Integer,
    "branch": fields.String,
    "cgpa": fields.Float,
    "year": fields.Integer,
    "user": fields.Nested(user_fields)
}

drive_fields = {
    "id": fields.Integer,
    "job_title": fields.String,
    "job_description": fields.String,
    "eligible_branch": fields.String,
    "minimum_cgpa": fields.Float,
    "eligible_year": fields.Integer,
    "deadline": fields.DateTime,
    "status": fields.String,
    "company_name": fields.String(attribute="company.company_name")
}

application_fields = {
    "id": fields.Integer,
    "date": fields.DateTime,
    "status": fields.String,
    "drive": fields.Nested(drive_fields),
    "student": fields.Nested(student_fields)
}