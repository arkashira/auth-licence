from dataclasses import dataclass
from enum import Enum
from functools import wraps
from http import HTTPStatus

class Role(Enum):
    FREE = 1
    PRO = 2
    ADMIN = 3

@dataclass
class User:
    id: int
    role: Role

def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(self, user, *args, **kwargs):
            if user.role != role:
                raise Exception(f"403 Forbidden: User role {user.role} is not {role}")
            return func(self, user, *args, **kwargs)
        return wrapper
    return decorator

class AuthLicence:
    def __init__(self):
        self.users = {}

    def signup(self, id, role):
        self.users[id] = User(id, role)

    @require_role(Role.FREE)
    def free_endpoint(self, user):
        return "Free endpoint"

    @require_role(Role.PRO)
    def pro_endpoint(self, user):
        return "Pro endpoint"

    @require_role(Role.ADMIN)
    def admin_endpoint(self, user):
        return "Admin endpoint"

    def get_user(self, id):
        return self.users.get(id)

    def call_endpoint(self, endpoint_name, user):
        endpoint = getattr(self, endpoint_name, None)
        if endpoint:
            return endpoint(user)
        else:
            raise Exception(f"Endpoint {endpoint_name} not found")
