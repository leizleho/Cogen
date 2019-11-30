from app.ma import ma
from app.models.project import Project
from app.mod_api.schemas.table import TableSchema


class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project
        load_only = ("user",)
        dump_only = ("id",)
        include_fk = True

    tables = ma.Nested(TableSchema, many=True)
