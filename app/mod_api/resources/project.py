from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
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

        return {"message": "project_not_found"}, 404

    @classmethod
    def post(cls):
        project_json = request.get_json()

        project = project_schema.load(project_json)

        try:
            project.save_to_db()
        except:
            return {"message": "An error occured while saving the project"}, 500

        return project_schema.dump(project), 201

    @classmethod
    def delete(cls, id: int):
        project = ProjectModel.find_by_id(id)
        if project:
            project.delete_from_db()
            return {"message": "Project deleted"}, 200

        return {"message": "Project not found"}, 404

    @classmethod
    def put(cls, id: int):
        project_json = request.get_json()
        project = ProjectModel.find_by_id(id)

        if project:
            project.user_id = project_json["user_id"]
            project.name = project_json["name"]
            project.description = project_json["description"]
            project.brand = project_json["brand"]
            project.logo = project_json["logo"]
            project.db_uri = project_json["db_uri"]

            try:
                project.save_to_db()
            except:
                return {"message": "An error occured while saving the project"}, 500

            return project_schema.dump(project), 200

        return {"message": "Project not found"}, 404


class Projects(Resource):
    @classmethod
    def get(cls):
        return {"projects": projects_schema.dump(ProjectModel.find_all())}, 200
