from app.ma import ma
from app.models.field import Field


class FieldSchema(ma.ModelSchema):
    class Meta:
        model = Field
        dump_only = ("id",)
        include_fk = True
