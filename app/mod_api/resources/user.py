from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from app.models.user import User as UserModel
from app.mod_api.schemas.user import UserSchema
from app.mod_api.blacklist import BLACKLIST

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()

        user = user_schema.load(user_json)

        if UserModel.find_by_email(user.email):
            return {"message": "Email is already registered."}, 400

        user.set_password(user.password_hash)
        user.save_to_db()

        return {"message": "Account created successfully"}, 201


class User(Resource):
    """
    This resource is for TESTING APP ONLY. We may not want to expose it to public users.
    """

    @classmethod
    def get(cls, id):
        user = UserModel.find_by_id(id)
        # user = UserModel.query.filter_by(id=id).first()
        if not user:
            return {"message": "User not found"}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, id: int):
        user = UserModel.find_by_id(id)
        if not user:
            return {"message": "User not found"}, 404

        user.delete_from_db()
        return {"message": "User deleted"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_email(user_data.email)

        if user and user.check_password(user_data.password_hash):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid email or password"}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        # jti is "JWT ID", a unique identifier for a JWT.
        jti = get_raw_jwt()["jti"]
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": f"User {user_id} successfully logged out."}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
