from app.ma import ma
from app.models.user import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        load_only = ("password_hash",)
        dump_only = ("id",)
