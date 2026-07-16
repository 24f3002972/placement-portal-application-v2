from ..models import Request, db
from .service_errors import ServiceError
from backend.extensions import cache
Model = Request

class RequestService():
    @staticmethod
    def get_all():
        return Model.query.all()
    
    @staticmethod
    def get_pending():
        return Model.query.filter_by(status="created").all()
    
    @staticmethod
    def get_by_id(id):
        request = Model.query.get(id)
        if not request:
            raise ServiceError("not found")
        return request
    
    @staticmethod
    def create(data):
        existing_request = Model.query.filter_by(
            user_id=data['user_id'],
            request_type=data['request_type'],
            status="created"
        ).first()
        if existing_request:
            raise ServiceError("Pending request already exists")
        request = Model(
            data=data['data'],
            user_id=data['user_id'],
            request_type=data['request_type'],
            status="created"
        )
        db.session.add(request)
        db.session.commit()
        return request

    @staticmethod
    def delete(id):
        request = Model.query.get(id)
        if not request:
            raise ServiceError("not found")
        db.session.delete(request)
        db.session.commit()
        return {"message": "Request with {id} deleted successfully"}

    @staticmethod
    def approve(id):
        request = RequestService.get_by_id(id)

        request.status = "approved"

        if request.request_type == "company_registration":
            request.user.active = True

        db.session.commit()
        cache.clear()
        return request
    
    @staticmethod
    def reject(id):
        request = RequestService.get_by_id(id)

        request.status = "rejected"

        db.session.commit()

        return request
         
