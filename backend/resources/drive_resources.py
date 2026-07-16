from flask import request, jsonify
from flask_restful import Resource, marshal, fields, reqparse
from backend.services.drive_services import DriveService
from .marshal_fields import drive_fields
from .resource_utils import validate_date
from flask_login import current_user
from flask_security import auth_required
from backend.extensions import cache

parser = reqparse.RequestParser()
parser.add_argument("job_title", type=str, required=True)
parser.add_argument("job_description", type=str, required=True)
parser.add_argument("eligible_branch", type=str, required=True)
parser.add_argument("minimum_cgpa", type=float, required=True)
parser.add_argument("eligible_year", type=int, required=True)
parser.add_argument("deadline", type=validate_date, required=True)

marshal_fields = drive_fields
"""/api/drive/:id"""
class DriveResource(Resource):
    def get(self, id):
        drive = DriveService.get_by_id(id)
        return marshal(drive, marshal_fields), 200
    
    @auth_required("token")
    def put(self, id):
        DriveService.get_by_id(id)

        args = parser.parse_args()
        args["id"] = id

        drive = DriveService.update(args)

        return marshal(drive, marshal_fields), 200
    
    @auth_required("token")
    def delete(self, id):
        drive = DriveService.get_by_id(id)
        if not drive:
            return {"message" : "not found"}, 404
        message = DriveService.delete(id)
        return message, 200
    
    @auth_required("token")
    def patch(self, id):
        drive = DriveService.get_by_id(id)
        if not drive:
            return {"message" : "not found"}, 404
        data = request.get_json()
        data["id"] = id
        drive = DriveService.update(data)
        return marshal(drive, marshal_fields), 200

"""/api/drive --> get, post"""
class DriveListResource(Resource):
    @auth_required("token")
    def get(self):

        if current_user.has_role("admin"):
            drives = DriveService.get_all()

        elif current_user.has_role("company"):
            drives = DriveService.get_company_drives(current_user.id)

        elif current_user.has_role("student"):
            drives = DriveService.get_approved()

        else:
            return {"message": "Unauthorized"}, 403

        return marshal(drives, marshal_fields), 200
    
    @auth_required("token")
    def post(self):

        args = parser.parse_args()

        args["company_id"] = current_user.id

        drive = DriveService.create(args)

        return {
            "message": "Drive created successfully",
            "drive_id": drive.id
        }, 201
    
class DriveSummaryResource(Resource):

    @auth_required("token")
    def get(self, id):

        summary = DriveService.get_summary(id)

        return summary, 200