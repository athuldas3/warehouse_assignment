from app.models.role import RoleMapping
from app import db
import uuid
from datetime import datetime


class RoleScripts:

    @staticmethod
    def create_roles():
        roles_to_add = [RoleMapping(role=role_name, CreatedDate=datetime.now())
                        for role_name in ["backendDeveloper", "PM", "RM", "frontendDeveloper"]]
        db.session.add_all(roles_to_add)
        db.session.commit()
