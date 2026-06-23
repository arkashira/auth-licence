import json
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class AuthConfig:
    """Dataclass to hold authentication configuration"""
    username: str
    password: str
    expiry: datetime

def setup_auth(config: AuthConfig) -> str:
    """Set up authentication with the given configuration"""
    if not isinstance(config, AuthConfig):
        raise TypeError("Invalid configuration")
    auth_data = {
        "username": config.username,
        "password": config.password,
        "expiry": config.expiry.isoformat()
    }
    return json.dumps(auth_data)

def validate_auth(auth_data: str) -> bool:
    """Validate the authentication data"""
    try:
        data = json.loads(auth_data)
        expiry = datetime.fromisoformat(data["expiry"])
        return expiry > datetime.now()
    except (json.JSONDecodeError, KeyError):
        return False

def integrate_with_web_app(auth_data: str) -> str:
    """Integrate the authentication system with the web app"""
    if validate_auth(auth_data):
        return "Authentication successful"
    else:
        return "Authentication failed"
