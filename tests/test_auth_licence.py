from src.auth_licence import setup_auth, validate_auth, integrate_with_web_app, AuthConfig
from datetime import datetime, timedelta
import pytest

def test_setup_auth():
    config = AuthConfig("test_user", "test_password", datetime.now() + timedelta(minutes=10))
    auth_data = setup_auth(config)
    assert "test_user" in auth_data
    assert "test_password" in auth_data

def test_validate_auth_valid():
    config = AuthConfig("test_user", "test_password", datetime.now() + timedelta(minutes=10))
    auth_data = setup_auth(config)
    assert validate_auth(auth_data)

def test_validate_auth_expired():
    config = AuthConfig("test_user", "test_password", datetime.now() - timedelta(minutes=10))
    auth_data = setup_auth(config)
    assert not validate_auth(auth_data)

def test_integrate_with_web_app_success():
    config = AuthConfig("test_user", "test_password", datetime.now() + timedelta(minutes=10))
    auth_data = setup_auth(config)
    assert integrate_with_web_app(auth_data) == "Authentication successful"

def test_integrate_with_web_app_failure():
    config = AuthConfig("test_user", "test_password", datetime.now() - timedelta(minutes=10))
    auth_data = setup_auth(config)
    assert integrate_with_web_app(auth_data) == "Authentication failed"

def test_setup_auth_invalid_config():
    with pytest.raises(TypeError):
        setup_auth("invalid_config")
