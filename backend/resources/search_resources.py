from flask_restful import Resource
from flask import request
from backend.models import Company, Student, Drive, User


class SearchResource(Resource):

    def get(self):

        query = request.args.get("q", "").strip()

        if query == "":
            return {
                "companies": [],
                "students": [],
                "drives": []
            }

        companies = Company.query.filter(
            Company.company_name.ilike(f"%{query}%")
        ).all()

        students = (
            Student.query
            .join(User)
            .filter(User.name.ilike(f"%{query}%"))
            .all()
        )

        drives = Drive.query.filter(
            Drive.job_title.ilike(f"%{query}%")
        ).all()

        return {

            "companies":[
                {
                    "id":company.id,
                    "name":company.company_name
                }
                for company in companies
            ],

            "students":[
                {
                    "id":student.id,
                    "name":student.user.name
                }
                for student in students
            ],

            "drives":[
                {
                    "id":drive.id,
                    "title":drive.job_title
                }
                for drive in drives
            ]

        },200