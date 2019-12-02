from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.models.table import Table as TableModel
from app.models.pagetemplate import PageTemplate as PageTemplateModel
from app.mod_api.schemas.pagetemplate import PageTemplateSchema

pagetemplate_schema = PageTemplateSchema()
pagetemplates_schema = PageTemplateSchema(many=True)


class PageTemplate(Resource):
    @classmethod
    def get(cls, id):
        pagetemplate = PageTemplateModel.find_by_id(id)
        if pagetemplate:
            return pagetemplate_schema.dump(pagetemplate), 200

        return {"error": "Page Template not found"}, 404

    @classmethod
    def post(cls):
        pagetemplate_json = request.get_json()

        try:
            pagetemplate = pagetemplate_schema.load(pagetemplate_json)
        except ValidationError as err:
            return err.messages

        # find the table for this page template
        table_id = pagetemplate_json["table_id"]
        table = TableModel.find_by_id(table_id)

        # if table exist, save the page template
        if table:
            try:
                pagetemplate.save_to_db()
            except:
                return {"error": "An error occured while saving the page template"}, 500

            return pagetemplate_schema.dump(pagetemplate), 201

        return {"error": "Table not found"}, 404

        @classmethod
        def delete(cls, id):
            pagetemplate = PageTemplateModel.find_by_id(id)
            if pagetemplate:
                pagetemplate.delete_from_db()
                return {"message": "Page Template Deleted"}, 200

            return {"error": "PageTemplate not found"}, 404

        @classmethod
        def put(cls, id):
            pagetemplate_json = request.get_json()
            pagetemplate = PageTemplateModel.find_by_id(id)

            if pagetemplate:
                for key, val in pagetemplate_json.items():
                    setattr(pagetemplate, key, val)

                try:
                    pagetemplate.save_to_db()
                except:
                    return {"error": "An error occured while saving the page template"}, 500

                return pagetemplate_schema.dump(pagetemplate), 200

            return {"error": "Page Template not found"}, 404


class PageTemplates(Resource):
    @classmethod
    def get(cls):
        return {"pagetemplates": pagetemplates_schema.dump(PageTemplateModel.find_all())}, 200
