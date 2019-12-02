from app.ma import ma
from app.models.pagetemplate import PageTemplate


class PageTemplateSchema(ma.ModelSchema):
    class Meta:
        model = PageTemplate
        dump_only = ("id",)
        include_fk = True
