from flask_restful import Resource, marshal
from flask import request
from ..services.company_services import CompanyService
from .marshal_fields import company_fields
from flask_security import auth_required
service = CompanyService


class CompanyListResource(Resource):

    def get(self):

        companies = service.get_all()

        return companies, 200


class CompanyResource(Resource):

    def get(self, id):

        company = service.get_by_id(id)

        return marshal(company, company_fields), 200

class CompanySummaryResource(Resource):

    @auth_required("token")

    def get(self, id):

        summary = CompanyService.get_summary(id)

        return summary, 200