from ..models import User, db
from .service_errors import ServiceError
from flask_security.utils import hash_password
import uuid
from datetime import datetime
from backend.extensions import cache

Model = User

class UserService():
    @staticmethod
    def get_all():
        return Model.query.all()
    
    @staticmethod
    def get_by_id(id):
        user = Model.query.get(id)
        if not user:
            raise ServiceError("not found")
        return user
    
    @staticmethod
    def create(data):
        existing_application = Model.query.filter_by(
            email=data["email"],
        ).first()
        if existing_application:
            raise ServiceError("user already exists")
        user = Model(
            email=data["email"],
            name=data["name"],
            password=hash_password(data["password"]),
            fs_uniquifier=str(uuid.uuid4())
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete(id):
        user = Model.query.get(id)
        if not user:
            raise ServiceError("not found")
        db.session.delete(user)
        db.session.commit()
        return {"message": "user with {id} deleted successfully"}

    @staticmethod
    def update(data):
        user = Model.query.get(data["id"])
        if not user:
            raise ServiceError("not found")
        for key, value in data.items():
            if hasattr(user, key) and key != "id":
                setattr(user, key, value)
        db.session.commit()
        return user
         
    @staticmethod
    def blacklist(id):
        user = User.query.get(id)

        if not user:
            raise ServiceError("User not found")

        user.active = False

    # If the user is a company, cancel all drives
        if user.company:

            for drive in user.company.drive:
                drive.status = "Closed"

        db.session.commit()
        cache.clear()
        return user


    @staticmethod
    def unblacklist(id):

        user = User.query.get(id)

        if not user:
            raise ServiceError("User not found")

        user.active = True

    # If this is a company, reopen valid drives
        if user.company:

            today = datetime.today()

            for drive in user.company.drive:

                if (
                    drive.status == "Closed"
                    and drive.deadline >= today
                ):
                    drive.status = "Approved"

        db.session.commit()
        cache.clear()
        return user