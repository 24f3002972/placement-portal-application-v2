from ..models import Application, Drive, Student, db
from .service_errors import ServiceError
from datetime import datetime
from backend.tasks import export_student_applications
from backend.extensions import cache
Model = Application

class ApplicationService():
    @staticmethod
    def get_all():
        return Model.query.all()
    
    @staticmethod
    def get_by_id(id):
        application = Model.query.get(id)
        if not application:
            raise ServiceError("not found")
        return application
    
    @staticmethod
    def create(data):
        drive = Drive.query.get(data["drive_id"])

        if not drive:
            raise ServiceError("Drive not found")
        if drive.status != "Approved":
            raise ServiceError("Drive is not available for applications")
        if drive.deadline < datetime.now():
            raise ServiceError("Application deadline has passed")
        student = Student.query.get(data["student_id"])

        if not student:
            raise ServiceError("Student not found")
        if student.branch != drive.eligible_branch:
            raise ServiceError("Branch not eligible")
        if student.cgpa < drive.minimum_cgpa:
            raise ServiceError("Minimum CGPA requirement not met")
        if student.year < drive.eligible_year:
            raise ServiceError("Year not eligible")
        existing_application = Model.query.filter_by(
            student_id=data["student_id"],
            drive_id=data["drive_id"]
        ).first()

        if existing_application:
            raise ServiceError("You have already applied for this drive")

        application = Model(
            student_id=data["student_id"],
            drive_id=data["drive_id"],
            status="Applied"
        )

        db.session.add(application)
        db.session.commit()
        cache.clear()
        return application

    @staticmethod
    def delete(id):
        application = Model.query.get(id)
        if not application:
            raise ServiceError("not found")
        db.session.delete(application)
        db.session.commit()
        return {"message": "application with {id} deleted successfully"}
    
         
    @staticmethod
    def get_company_applications(company_id):
        return (
            Application.query
            .join(Drive)
            .filter(Drive.company_id == company_id)
            .all()
        )
    
    @staticmethod
    def update_status(application_id, company_id, status):
        application = Application.query.get(application_id)

        if not application:
            raise ServiceError("Application not found")
        
        drive = application.drive

        if drive.company_id != company_id:
            raise ServiceError("Unauthorized")
        valid_status = {
            "Applied",
            "Shortlisted",
            "Selected",
            "Rejected"
        }

        if status not in valid_status:
            raise ServiceError("Invalid status")

        application.status = status

        db.session.commit()

        return application
    
    @staticmethod
    def get_student_applications(student_id):
        return (
            Application.query
            .filter_by(student_id=student_id)
            .all()
        )
    
    @staticmethod
    def export(student_id):

        task = export_student_applications.delay(student_id)

        return task.id
    
    @staticmethod
    def get_drive_applications(company_id, drive_id):

        return (
        Application.query
        .join(Drive)
        .filter(
            Drive.company_id == company_id,
            Drive.id == drive_id
        )
        .all()
    )