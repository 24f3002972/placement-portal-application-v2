from flask import request, jsonify
from flask_restful import Resource, marshal, fields, reqparse
from ..services.application_service import ApplicationService
from .marshal_fields import application_fields
from flask_security import auth_required
from flask_login import current_user
from ..models import Application
from ..services.service_errors import ServiceError

parser = reqparse.RequestParser()
parser.add_argument("drive_id", type=int, required=True)
marshal_fields = application_fields
service = ApplicationService

"""/api/application/:id"""
class ApplicationResource(Resource):
    def get(self, id):
        application = service.get_by_id(id)
        return marshal (application, marshal_fields), 200
    
    @auth_required("token")
    def delete(self, id):
        application = service.get_by_id(id)
        if not application:
            return {"message" : "not found"}, 404
        if current_user.has_role("student"):
            if application.student_id != current_user.id:
                return {"message": "Unauthorized"}, 403

        elif not current_user.has_role("admin"):
            return {"message": "Unauthorized"}, 403
        message = service.delete(id)
        return message, 200
    
    @auth_required("token")
    def patch(self, id):

        if not (
            current_user.has_role("company")
            or current_user.has_role("admin")
        ):
            return {"message": "Unauthorized"}, 403

        data = request.get_json()

        application = service.update_status(
            id,
            current_user.id,
            data["status"]
        )

        return marshal(application, marshal_fields), 200

    @staticmethod
    def get_student_applications(student_id):
        return (
            Application.query
            .filter_by(student_id=student_id)
            .all()
        )    
"""/api/application --> get, post"""
class ApplicationListResource(Resource):
    @auth_required("token")
    def post(self):
        if not current_user.has_role("student"):
            return {
                "message": "Only students can apply for drives"
            }, 403

        args = parser.parse_args()

        args["student_id"] = current_user.id
        try:
            application = service.create(args)
        except ServiceError as e:
            return {"message": str(e)}, 400
        return marshal(application, marshal_fields), 201
    
    @auth_required("token")
    def get(self):
        if current_user.has_role("admin"):
            applications = service.get_all()

        elif current_user.has_role("company"):
            applications = service.get_company_applications(current_user.id)

        elif current_user.has_role("student"):
            applications = service.get_student_applications(current_user.id)

        else:
            return {"message": "Unauthorized"}, 403

        return marshal(applications, marshal_fields), 200
    
class ApplicationExportResource(Resource):

    @auth_required("token")
    def post(self):

        if not current_user.has_role("student"):
            return {
                "message": "Only students can export applications."
            }, 403

        task_id = ApplicationService.export(current_user.student.id)

        return {
            "message": "Export started successfully.",
            "task_id": task_id
        }, 202
    
class DriveApplicationListResource(Resource):

    @auth_required("token")
    def get(self, drive_id):

        if not current_user.has_role("company"):
            return {
                "message":"Unauthorized"
            },403

        applications = service.get_drive_applications(

            current_user.id,

            drive_id

        )

        return marshal(

            applications,

            marshal_fields

        ),200