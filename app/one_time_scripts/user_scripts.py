from app.models.role import RoleMapping
from app import db
from app.models.user import User
from app.one_time_scripts.role_scripts import RoleScripts
import uuid
from datetime import datetime


class UserScripts:

    @staticmethod
    def generate_password_hash(password):
        return "$2b$12$KE.vUU8OjKM6MdNU9oErWO6m/o/scktZIyNEbi0twfSbC1.eWsMUu"  # password for User@123

    @staticmethod
    def get_role_id(role):
        role_obj = RoleMapping.query.filter_by(role=role).first()

        if not role_obj:
            # If the role doesn't exist, create all roles
            RoleScripts().create_roles()

            # Retrieve the role again after creation
            role_obj = RoleMapping.query.filter_by(role=role).first()

        return role_obj

    def get_user_objects(self):
        """
        generating all role user using default password, username as role, setting email as role@gmail.com
        """
        return [User(username=role, role=self.get_role_id(role).id, email=f"{role}@gmail.com",
                     password_hash=self.generate_password_hash("User@123"), CreatedDate=datetime.now())
                for role in ['backendDeveloper', 'PM', 'RM', 'frontendDeveloper']]

    def create_user(self):

        # fetch user data
        users_objects = self.get_user_objects()

        # Use bulk_save_objects to efficiently add multiple records in a single database round-trip
        try:
            # Bulk save the User objects
            db.session.bulk_save_objects(users_objects)
            db.session.commit()
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()


