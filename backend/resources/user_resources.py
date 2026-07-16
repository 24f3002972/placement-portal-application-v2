from flask import request, jsonify
from flask_restful import Resource, marshal, fields, reqparse
from ..services.user_service import UserService
from .marshal_fields import user_fields
from .resource_utils import validate_date
from flask_security import current_user
from flask_security.decorators import roles_required
from flask import request
from flask_security import auth_required

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True)
parser.add_argument("email", type=str, required=True)
parser.add_argument("password", type=str, required=False)

marshal_fields = user_fields
service = UserService

"""/api/user/:id"""
class UserResource(Resource):
    #--> only admin
    def get(self, id):
        if (current_user.has_role("company") or current_user.has_role("student")) and current_user.id != id:
            return {"message": "not authorized"}, 401
        user = service.get_by_id(id)
        return marshal (user, marshal_fields), 200

    def put(self, id):
        if (current_user.has_role("company") or current_user.has_role("student")) and current_user.id != id:
            return {"message": "not authorized"}, 401
        user = service.get_by_id(id)
        if not user:
            return {"message" : "not found"}, 404
        args = parser.parse_args()
        args["id"] = id
        user = service.update(args)
        return marshal(user, user_fields), 200
    
    def delete(self, id):
        user = service.get_by_id(id)
        if not user:
            return {"message" : "not found"}, 404
        message = service.delete(id)
        return message, 200
    
    @auth_required("token")
    def patch(self, id):

        user = service.get_by_id(id)

        if not user:
            return {"message": "not found"}, 404

        data = request.get_json()

    # ---------- Admin blacklist / activate ----------
        if current_user.has_role("admin") and "action" in data:

            if data["action"] == "blacklist":
                user = service.blacklist(id)

            elif data["action"] == "unblacklist":
                user = service.unblacklist(id)

            else:
                return {"message": "Invalid action"}, 400

            return marshal(user, marshal_fields), 200

    # ---------- Normal profile update ----------
        if (
            (current_user.has_role("company") or current_user.has_role("student"))
            and current_user.id != id
        ):
            return {"message": "not authorized"}, 401

        data["id"] = id

        user = service.update(data)

        return marshal(user, marshal_fields), 200

"""/api/user --> get, post"""
class UserListResource(Resource):
    @roles_required("admin")
    def get(self):
        users = service.get_all()
        return marshal(users, marshal_fields)
