from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.models.field import Field as FieldModel
from app.models.table import Table as TableModel
from app.mod_api.schemas.field import FieldSchema


field_schema = FieldSchema()
fields_schema = FieldSchema(many=True)


class Field(Resource):
    @classmethod
    def get(cls, id):
        field = FieldModel.find_by_id(id)
        if field:
            return field_schema.dump(field), 200

        return {"error": "Field not found"}, 404

    @classmethod
    def post(cls):
        field_json = request.get_json()

        try:
            field = field_schema.load(field_json)
        except ValidationError as err:
            return err.messages

        # find the table for this field
        table_id = field_json["table_id"]
        table = TableModel.find_by_id(table_id)

        # if table exist, save the field
        if table:
            try:
                field.save_to_db()
            except:
                return {"error": "An error occured while saving the field"}, 500

            return field_schema.dump(field), 201

        return {"error": "Table not found"}, 404

    @classmethod
    def delete(cls, id):
        field = FieldModel.find_by_id(id)
        if field:
            field.delete_from_db()
            return {"message": "field deleted"}, 200

        return {"error": "Field not found"}, 404

    @classmethod
    def put(cls, id):
        field_json = request.get_json()
        field = FieldModel.find_by_id(id)

        if field:
            for key, val in field_json.items():
                setattr(field, key, val)

            try:
                field.save_to_db()
            except:
                return {"error": "An error occured while saving the field"}, 500

            return field_schema.dump(field), 200

        return {"error": "Field not found"}, 404


class Fields(Resource):
    @classmethod
    def get(cls):
        return {"fields": fields_schema.dump(FieldModel.find_all())}, 200
