"/login"
"/register"

from flask import Blueprint, request, jsonify
from flask_security.utils import verify_password, hash_password
from ..models import User, db, Student, Company, Request
from flask import current_app
from backend.services.request_services import RequestService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    print("Received login data:", data)
    print("Email received:", repr(email))
    password = data["password"]
    if (not email or not password):
        return jsonify({"message": "invalid input"}), 400
    user = User.query.filter_by(email = email).first()
    if not user:
        return jsonify({
            "message": "User not found"
        }), 404
    if not user.active:
        return jsonify({"message": "account inactive"}), 403
    if not verify_password(password, user.password):
        return jsonify({"message": "wrong password"}), 400
    return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.roles[0].name,
            "token": user.get_auth_token()
        }), 200 

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    role_name = data['role']
    active = True
    if not name or not email or not password or not role_name in ["company", "student"]:
        return jsonify({"message": "invalid inputs"})
    if User.query.filter_by(email = email).first():
        return {"message": "user already exists"}, 400
    if role_name == "company":
        active = False
    datastore = current_app.datastore

    try:
        datastore.create_user(name=name, email=email, password=hash_password(password), active=active)
        db.session.flush()
        role = datastore.find_role(role_name)
        user = datastore.find_user(email = email)
        datastore.add_role_to_user(user, role)
        if role_name == 'student':
            student = Student(
                id=user.id,
                branch=data["branch"],
                cgpa=data["cgpa"],
                year=data["year"]
            )
            db.session.add(student)
        elif role_name == 'company':
            company = Company(
                id=user.id,
                company_name=data["company_name"],
                hr_contact=data["hr_contact"],
                website=data["website"]
            )
            db.session.add(company)
            RequestService.create({
                "user_id": user.id,
                "request_type": "company_registration",
                "data": {
                    "company_name": company.company_name,
                    "hr_contact": company.hr_contact,
                    "website": company.website
                }
            })
        db.session.commit()
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": role_name
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "registration failed",
            "error": str(e)
        }), 400


