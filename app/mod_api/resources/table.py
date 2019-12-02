from flask import request
from flask_restful import Resource
from app.models.table import Table as TableModel
from app.models.project import Project as ProjectModel
from app.mod_api.schemas.table import TableSchema
from marshmallow import ValidationError

table_schema = TableSchema()
tables_schema = TableSchema(many=True)


class Table(Resource):
    @classmethod
    def get(cls, id):
        table = TableModel.find_by_id(id)
        if table:
            return table_schema.dump(table), 200

        return {"error": "Table not found"}, 404

    @classmethod
    def post(cls):
        table_json = request.get_json()

        try:
            table = table_schema.load(table_json)
        except ValidationError as err:
            return err.messages

        # find the project for this table
        project_id = table_json["project_id"]
        project = ProjectModel.find_by_id(project_id)

        # if project exist, save the table
        if project:
            try:
                table.save_to_db()
            except:
                return {"message": "An error occured while saving the table"}, 500

            return table_schema.dump(table), 201

        return {"error": "Project not found"}, 404

    @classmethod
    def delete(cls, id):
        table = TableModel.find_by_id(id)
        if table:
            table.delete_from_db()
            return {"message": "table deleted"}, 200

        return {"error": "table not found"}, 404

    @classmethod
    def put(cls, id):
        table_json = request.get_json()
        table = TableModel.find_by_id(id)

        if table:
            for key, val in table_json.items():
                setattr(table, key, val)

            try:
                table.save_to_db()
            except:
                return {"error": "An error occured while saving the project"}, 500

            return table_schema.dump(table), 200

        return {"error": "Table not found"}, 404


class Tables(Resource):
    @classmethod
    def get(cls):
        return {"tables": tables_schema.dump(TableModel.find_all())}, 200
