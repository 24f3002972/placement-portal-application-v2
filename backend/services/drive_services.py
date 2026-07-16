from ..models import Drive, db, Company
from .service_errors import ServiceError
from backend.extensions import cache

class DriveService():
    @staticmethod
    def get_all():
        return Drive.query.all()
    
    @staticmethod
    def get_approved():
        return Drive.query.filter_by(status="Approved").all()
    
    @staticmethod
    def get_by_id(id):
        drive = Drive.query.get(id)
        if not drive:
            raise ServiceError("not found")
        return drive
    
    @staticmethod
    def create(data):
        existing_drive = Drive.query.filter_by(
            company_id=data["company_id"],
            job_title=data["job_title"],
            deadline=data["deadline"]
        ).first()
        if existing_drive:
            raise ServiceError("Drive already exists")
        drive = Drive(
            company_id=data["company_id"],
            job_title=data["job_title"],
            job_description=data.get("job_description"),
            eligible_branch=data["eligible_branch"],
            minimum_cgpa=data["minimum_cgpa"],
            eligible_year=data["eligible_year"],
            deadline=data["deadline"],
            status="Approved"
        )
        db.session.add(drive)
        db.session.commit()
        cache.clear()
        return drive

    @staticmethod
    def delete(id):
        drive = Drive.query.get(id)
        if not drive:
            raise ServiceError("not found")
        db.session.delete(drive)
        db.session.commit()
        cache.clear()
        return {"message": "Drive with {id} deleted successfully"}

    @staticmethod
    def update(data):
        drive = Drive.query.get(data["id"])
        if not drive:
            raise ServiceError("not found")
        for key, value in data.items():
            if hasattr(drive, key) and key != "id":
                setattr(drive, key, value)
        db.session.commit()
        cache.clear()
        return drive
    
    @staticmethod
    def get_company_drives(company_id):
        return Drive.query.filter_by(company_id=company_id).all()
    
    @staticmethod
    def get_summary(id):

        drive = DriveService.get_by_id(id)

        company = Company.query.get(drive.company_id)

        return {

            "id": drive.id,

            "job_title": drive.job_title,

            "job_description": drive.job_description,

            "eligible_branch": drive.eligible_branch,

            "minimum_cgpa": float(drive.minimum_cgpa),

            "eligible_year": drive.eligible_year,

            "deadline": drive.deadline.strftime("%d-%m-%Y"),

            "status": drive.status,

            "company_name": company.company_name

        }