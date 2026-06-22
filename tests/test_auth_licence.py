from auth_licence import AuthLicence, RevenueData

def test_track_revenue():
    auth_licence = AuthLicence()
    auth_licence.track_revenue(10.0, 1)
    assert len(auth_licence.revenue_data) == 1
    assert auth_licence.revenue_data[0].revenue == 10.0
    assert auth_licence.revenue_data[0].user_id == 1

def test_get_analytics():
    auth_licence = AuthLicence()
    auth_licence.track_revenue(10.0, 1)
    auth_licence.track_revenue(20.0, 2)
    total_revenue, user_activity = auth_licence.get_analytics()
    assert total_revenue == 30.0
    assert user_activity == {1: 10.0, 2: 20.0}

def test_detect_fraud():
    auth_licence = AuthLicence()
    for _ in range(11):
        auth_licence.track_revenue(10.0, 1)
    fraud_users = auth_licence.detect_fraud()
    assert fraud_users == {1: 11}
