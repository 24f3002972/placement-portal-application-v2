from ..models import Company, db, Drive
from .service_errors import ServiceError
from backend.extensions import cache
Model = Company


class CompanyService:

    @staticmethod
    @cache.memoize(timeout=60)
    def get_all():

        companies = Company.query.all()

        result = []

        for company in companies:

            result.append({

                "id": company.id,

                "company_name": company.company_name,

                "website": company.website,

                "hr_contact": company.hr_contact,

                "active": company.user.active,

                "user_id": company.user.id

            })

        return result

    @staticmethod
    def get_by_id(id):
        company = Model.query.get(id)

        if not company:
            raise ServiceError("Company not found")

        return company
    
    @staticmethod
    def get_summary(id):

        company = CompanyService.get_by_id(id)

        drives = Drive.query.filter_by(
            company_id=id
        ).all()
 
        drive_list = []

        for drive in drives:

            drive_list.append({

                "id": drive.id,

                "job_title": drive.job_title,

                "deadline": drive.deadline.strftime("%d-%m-%Y"),

                "status": drive.status

            })

        return {

            "id": company.id,

            "company_name": company.company_name,

            "website": company.website,

            "hr_contact": company.hr_contact,

            "status": "Active" if company.user.active else "Inactive",

            "overview": (
                f"{company.company_name} is actively recruiting through the "
                f"Placement Portal. Students can explore ongoing placement "
                f"drives, check eligibility criteria, and apply online."
            ),

            "drives": drive_list

        }