import sqlite3
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


@dataclass
class Incident:
    timestamp: datetime
    user: str
    ip: str
    reason: str

    def to_record(self) -> tuple:
        """Convert the incident to a SQLite‑compatible record."""
        return (self.timestamp.isoformat(), self.user, self.ip, self.reason)


class IncidentManager:
    """
    Manages anti‑piracy incidents and user disabling.

    Incidents are stored in a Redis‑like dict (self._redis) and persisted to a
    SQLite database (self._db_path). Disabled users are tracked similarly.
    """

    def __init__(self, redis_client: Optional[Dict[str, Any]] = None, db_path: str = ":memory:"):
        # Simple in‑memory Redis mock: a dict with two keys.
        self._redis: Dict[str, Any] = redis_client if redis_client is not None else {"incidents": [], "disabled": set()}
        self._db_path = db_path
        self._ensure_tables()

    # --------------------------------------------------------------------- #
    # SQLite helpers
    # --------------------------------------------------------------------- #
    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_tables(self) -> None:
        """Create tables if they do not exist."""
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS incidents (
                    timestamp TEXT NOT NULL,
                    user TEXT NOT NULL,
                    ip TEXT NOT NULL,
                    reason TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS disabled_users (
                    user TEXT PRIMARY KEY
                )
                """
            )

    # --------------------------------------------------------------------- #
    # Incident handling
    # --------------------------------------------------------------------- #
    def add_incident(self, incident: Incident) -> None:
        """
        Record a new incident.

        The incident is appended to the Redis list and inserted into SQLite.
        """
        if not incident.user:
            raise ValueError("User must be a non‑empty string")
        # Store in Redis mock
        self._redis["incidents"].append(incident)
        # Persist to SQLite
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO incidents (timestamp, user, ip, reason) VALUES (?, ?, ?, ?)",
                incident.to_record(),
            )

    def get_incidents(self) -> List[Dict[str, Any]]:
        """
        Return all incidents as a list of dicts ordered by timestamp ascending.
        """
        with self._connect() as conn:
            rows = conn.execute("SELECT timestamp, user, ip, reason FROM incidents ORDER BY timestamp").fetchall()
        return [
            {
                "timestamp": datetime.fromisoformat(row["timestamp"]),
                "user": row["user"],
                "ip": row["ip"],
                "reason": row["reason"],
            }
            for row in rows
        ]

    # --------------------------------------------------------------------- #
    # User disabling
    # --------------------------------------------------------------------- #
    def disable_user(self, user: str) -> None:
        """
        Mark a user as disabled.

        The user identifier is added to the Redis set and persisted in SQLite.
        """
        if not user:
            raise ValueError("User must be a non‑empty string")
        self._redis["disabled"].add(user)
        with self._connect() as conn:
            conn.execute("INSERT OR IGNORE INTO disabled_users (user) VALUES (?)", (user,))

    def is_user_disabled(self, user: str) -> bool:
        """
        Check whether a user is disabled.
        """
        if user in self._redis["disabled"]:
            return True
        with self._connect() as conn:
            row = conn.execute("SELECT 1 FROM disabled_users WHERE user = ?", (user,)).fetchone()
        return row is not None
