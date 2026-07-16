from ..models import Student, db
from .service_errors import ServiceError
from backend.extensions import cache
Model = Student


class StudentService:

    @staticmethod
    def get_all():
        return Model.query.all()

    @staticmethod
    def get_by_id(id):
        student = Model.query.get(id)

        if not student:
            raise ServiceError("Student not found")

        return student
    
    @staticmethod
    def update(data):

        student = Model.query.get(data["id"])

        if not student:
            raise ServiceError("Student not found")

        if "branch" in data:
            student.branch = data["branch"]

        if "cgpa" in data:
            student.cgpa = data["cgpa"]

        if "year" in data:
            student.year = data["year"]

        db.session.commit()

        return student