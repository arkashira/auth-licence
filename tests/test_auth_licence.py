import os
import tempfile
from datetime import datetime, timedelta

import pytest

from auth_licence import Incident, IncidentManager


@pytest.fixture
def temp_db_path():
    """Create a temporary file for SQLite persistence."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    os.remove(path)


@pytest.fixture
def manager(temp_db_path):
    """Provide an IncidentManager with a fresh in‑memory Redis mock."""
    return IncidentManager(redis_client={"incidents": [], "disabled": set()}, db_path=temp_db_path)


def test_add_and_retrieve_incident(manager):
    inc = Incident(
        timestamp=datetime.utcnow(),
        user="alice",
        ip="192.0.2.1",
        reason="credential sharing detected",
    )
    manager.add_incident(inc)

    incidents = manager.get_incidents()
    assert len(incidents) == 1
    retrieved = incidents[0]
    assert retrieved["user"] == "alice"
    assert retrieved["ip"] == "192.0.2.1"
    assert retrieved["reason"] == "credential sharing detected"
    # timestamps may differ slightly due to serialization; compare within 1 second
    assert abs((retrieved["timestamp"] - inc.timestamp).total_seconds()) < 1


def test_add_incident_invalid_user(manager):
    inc = Incident(timestamp=datetime.utcnow(), user="", ip="10.0.0.1", reason="test")
    with pytest.raises(ValueError, match="User must be a non‑empty string"):
        manager.add_incident(inc)


def test_disable_user_and_check(manager):
    manager.disable_user("bob")
    assert manager.is_user_disabled("bob") is True
    # A user not disabled should return False
    assert manager.is_user_disabled("charlie") is False


def test_disable_user_invalid(manager):
    with pytest.raises(ValueError, match="User must be a non‑empty string"):
        manager.disable_user("")


def test_persistence_across_instances(temp_db_path):
    # First manager writes data
    mgr1 = IncidentManager(redis_client={"incidents": [], "disabled": set()}, db_path=temp_db_path)
    inc = Incident(timestamp=datetime.utcnow(), user="dave", ip="203.0.113.5", reason="share")
    mgr1.add_incident(inc)
    mgr1.disable_user("dave")

    # New manager reads from same SQLite file (Redis mock starts empty)
    mgr2 = IncidentManager(redis_client={"incidents": [], "disabled": set()}, db_path=temp_db_path)
    incidents = mgr2.get_incidents()
    assert len(incidents) == 1
    assert incidents[0]["user"] == "dave"
    assert mgr2.is_user_disabled("dave") is True
