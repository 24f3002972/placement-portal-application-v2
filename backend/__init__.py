from .auth_resources import auth_bp
from flask_restful import Api
from flask import Blueprint
from .auth_resources import auth_bp 
from .drive_resources import DriveListResource, DriveResource, DriveSummaryResource
from .application_resources import ApplicationListResource, ApplicationResource, ApplicationExportResource, DriveApplicationListResource
from .user_resources import UserListResource, UserResource
from .request_resources import RequestListResource, RequestResource
from .company_resources import CompanyListResource, CompanyResource, CompanySummaryResource
from .student_resources import StudentListResource, StudentResource
from .search_resources import SearchResource

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)
api.add_resource(DriveListResource, "/drive")
api.add_resource(DriveResource, "/drive/<int:id>")
api.add_resource(DriveSummaryResource, "/drive/<int:id>/summary")
api.add_resource(DriveApplicationListResource,"/drive/<int:drive_id>/applications")
api.add_resource(ApplicationListResource, "/application")
api.add_resource(ApplicationResource, "/application/<int:id>")
api.add_resource(ApplicationExportResource,"/application/export")

api.add_resource(UserListResource, "/user")
api.add_resource(UserResource, "/user/<int:id>")

api.add_resource(RequestListResource, "/request")
api.add_resource(RequestResource, "/request/<int:id>")

api.add_resource(CompanyListResource, "/company")
api.add_resource(CompanyResource, "/company/<int:id>")
api.add_resource(CompanySummaryResource, "/company/<int:id>/summary")

api.add_resource(StudentListResource, "/student")
api.add_resource(StudentResource, "/student/<int:id>")

api.add_resource(SearchResource, "/search")