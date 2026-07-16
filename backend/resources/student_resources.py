from flask_restful import Resource, marshal
from flask import request
from flask_security import auth_required, current_user
from ..services.student_services import StudentService
from .marshal_fields import student_fields

service = StudentService


class StudentListResource(Resource):

    def get(self):

        students = service.get_all()

        return marshal(students, student_fields), 200


class StudentResource(Resource):

    def get(self, id):

        student = service.get_by_id(id)

        return marshal(student, student_fields), 200
    
    @auth_required("token")
    def put(self, id):

        if (
            current_user.has_role("student")
            and current_user.id != id
        ):
            return {
                "message": "Unauthorized"
            }, 403

        data = request.get_json()

        data["id"] = id

        student = service.update(data)

        return marshal(student, student_fields), 200