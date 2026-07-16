from flask import request
from flask_restful import Resource

from backend.services.request_services import RequestService
from backend.services.service_errors import ServiceError

class RequestListResource(Resource):

    def get(self):
        requests = RequestService.get_pending()

        result = []

        for req in requests:
            result.append({
                "id": req.id,
                "request_type": req.request_type,
                "status": req.status,
                "user_id": req.user_id,
                "data": req.data
            })

        return result, 200
    
class RequestResource(Resource):

    def patch(self, id):

        body = request.get_json()

        action = body.get("action")

        try:

            if action == "approve":
                req = RequestService.approve(id)

            elif action == "reject":
                req = RequestService.reject(id)

            else:
                return {"message": "Invalid action"}, 400

            return {
                "message": f"Request {action}d successfully"
            }, 200

        except ServiceError as e:
            return {
                "message": str(e)
            }, 404  