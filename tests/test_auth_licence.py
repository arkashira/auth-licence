from auth_licence import AuthLicence, Role, User

def test_signup():
    auth = AuthLicence()
    auth.signup(1, Role.FREE)
    assert auth.get_user(1).role == Role.FREE

def test_free_endpoint():
    auth = AuthLicence()
    auth.signup(1, Role.FREE)
    user = auth.get_user(1)
    assert auth.free_endpoint(user) == "Free endpoint"

def test_pro_endpoint():
    auth = AuthLicence()
    auth.signup(1, Role.PRO)
    user = auth.get_user(1)
    assert auth.pro_endpoint(user) == "Pro endpoint"

def test_admin_endpoint():
    auth = AuthLicence()
    auth.signup(1, Role.ADMIN)
    user = auth.get_user(1)
    assert auth.admin_endpoint(user) == "Admin endpoint"

def test_unauthorized_access():
    auth = AuthLicence()
    auth.signup(1, Role.FREE)
    user = auth.get_user(1)
    try:
        auth.pro_endpoint(user)
        assert False, "Expected 403 Forbidden"
    except Exception as e:
        assert str(e) == "403 Forbidden: User role Role.FREE is not Role.PRO"

def test_call_endpoint():
    auth = AuthLicence()
    auth.signup(1, Role.FREE)
    user = auth.get_user(1)
    assert auth.call_endpoint("free_endpoint", user) == "Free endpoint"

def test_call_nonexistent_endpoint():
    auth = AuthLicence()
    auth.signup(1, Role.FREE)
    user = auth.get_user(1)
    try:
        auth.call_endpoint("nonexistent_endpoint", user)
        assert False, "Expected exception"
    except Exception as e:
        assert str(e) == "Endpoint nonexistent_endpoint not found"
