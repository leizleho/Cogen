from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from marshmallow import ValidationError
from app.models.project import Project as ProjectModel
from app.mod_api.schemas.project import ProjectSchema

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


class Project(Resource):
    @classmethod
    def get(cls, id: int):
        project = ProjectModel.find_by_id(id)
        if project:
            return project_schema.dump(project), 200

        return {"error": "project_not_found"}, 404

    @classmethod
    def post(cls):
        project_json = request.get_json()

        try:
            project = project_schema.load(project_json)
        except ValidationError as err:
            return err.messages

        try:
            project.save_to_db()
        except:
            return {"error": "An error occured while saving the project"}, 500

        return project_schema.dump(project), 201

    @classmethod
    def delete(cls, id: int):
        project = ProjectModel.find_by_id(id)
        if project:
            project.delete_from_db()
            return {"message": "Project deleted"}, 200

        return {"error": "Project not found"}, 404

    @classmethod
    def put(cls, id: int):
        project_json = request.get_json()
        project = ProjectModel.find_by_id(id)

        if project:
            for key, val in project_json.items():
                setattr(project, key, val)

            try:
                project.save_to_db()
            except:
                return {"error": "An error occured while saving the project"}, 500

            return project_schema.dump(project), 200

        return {"error": "Project not found"}, 404


class Projects(Resource):
    @classmethod
    def get(cls):
        return {"projects": projects_schema.dump(ProjectModel.find_all())}, 200
