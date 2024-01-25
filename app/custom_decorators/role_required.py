from functools import wraps
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import cast, String, Integer
from app.models.role import RoleMapping
from app.models.user import User


def roles_required(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()

            # Check if the current user has any of the required roles
            user = User.query.filter_by(email=current_user_id).first()
            role = RoleMapping.query.filter_by(id=cast(user.role, Integer)).first()
            try:
                if not user or not role or not user.role or str(role) not in required_roles:
                    return {'error': f'Unauthorized: Only {", ".join(required_roles)} can access this API'}, 403
            except Exception as e:
                print(f"The exception in decorator role required is: {e}")
                return {'error': f'Unauthorized: Only {", ".join(required_roles)} can access this API'}, 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
