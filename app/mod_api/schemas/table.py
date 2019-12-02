from app.ma import ma
from app.models.table import Table
from app.mod_api.schemas.field import FieldSchema


class TableSchema(ma.ModelSchema):
    fields = ma.Nested(FieldSchema, many=True)

    class Meta:
        model = Table
        dump_only = ("id",)
        include_fk = True
