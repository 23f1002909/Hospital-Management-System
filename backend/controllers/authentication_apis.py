from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils

from controllers.user_datastore import user_datastore

class LoginAPI(Resource):
    def post(self):
        login_credentials = request.get_json()

        if not login_credentials:
            result = {
                "message" : "Login Credentials Req."
            }

            return make_response(jsonify(result), 400)
        
        email = login_credentials.get("email", None)
        password = login_credentials.get("password", None)

        if not email or not password:
            result = {
                "message" : "Username and Password Req."
            }

            return make_response(jsonify(result), 400)

        user = user_datastore.find_user(email = email)

        if not user:
            result = {
                "message" : "User not found"
            }

            return make_response(jsonify(result), 404)
        
        if not utils.verify_password(password, user.password):
            result = {
                "message" : "Incorrect Password"
            }
            return make_response(jsonify(result), 404)

        auth_token = user.get_auth_token()

        utils.login_user(user)

        response = {
            "message" : "Login Successful",
            "user details" : {
                "email" : user.email,
                "roles" :[role.name for role in user.roles],
                "auth_token" : auth_token
                }
        }

        return make_response(jsonify(response), 200)