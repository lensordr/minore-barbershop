"""
Bug Condition Exploration Tests - Sentry Connection Pool Fix

These tests confirm the bug EXISTS on unfixed code.
They assert the BUGGY behavior (422 RequestValidationError for invalid service_id).
After the fix is applied, these tests MUST FAIL (proving the bug is gone).

Validates: Requirements 1.2
"""
import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set DATABASE_URL so the module doesn't raise RuntimeError
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test_db")

# Mock psycopg and the database engine creation before importing main
# This is necessary because psycopg binary is not available in the test environment
# and the bug we're testing (422 for invalid service_id) occurs at the FastAPI
# validation layer BEFORE any database interaction.
import unittest.mock

# Create mock for the database module
mock_engine = MagicMock()
mock_session_local = MagicMock()


def mock_get_db():
    db = MagicMock()
    try:
        yield db
    finally:
        pass


# Patch database_postgres module before importing main
with unittest.mock.patch.dict(sys.modules, {
    'psycopg': MagicMock(),
    'psycopg.pq': MagicMock(),
}):
    # We need to mock the entire database_postgres module
    import importlib
    import types

    # Create a fake database_postgres module
    fake_db_module = types.ModuleType('database_postgres')
    fake_db_module.get_db = mock_get_db
    fake_db_module.engine = mock_engine
    fake_db_module.SessionLocal = mock_session_local
    sys.modules['database_postgres'] = fake_db_module

    from main import app

from fastapi.testclient import TestClient

# raise_server_exceptions=False so we get HTTP responses even for 500 errors
# (needed for service_id=0 test which reaches the mocked DB layer)
client = TestClient(app, raise_server_exceptions=False)


class TestInvalidServiceIdValidationError:
    """
    Bug Condition: When the frontend sends a non-integer service_id
    (e.g., "undefined", "abc") to /api/available-times/{barber_id}/{service_id},
    FastAPI raises a 422 RequestValidationError instead of handling it gracefully.

    These tests CONFIRM the bug exists by asserting the 422 response.
    After the fix, the endpoint will return 200 with [], causing these tests to FAIL.
    """

    def test_undefined_service_id_returns_422(self):
        """
        Bug: Frontend sends literal "undefined" as service_id when no service selected.
        Expected on UNFIXED code: 422 RequestValidationError
        Expected on FIXED code: 200 with [] (test will FAIL after fix)
        """
        response = client.get("/api/available-times/1/undefined")
        assert response.status_code == 422, (
            f"Expected 422 (bug condition) but got {response.status_code}. "
            "If this is 200, the bug may already be fixed."
        )

    def test_alphabetic_service_id_returns_422(self):
        """
        Bug: Non-numeric string "abc" as service_id triggers validation error.
        Expected on UNFIXED code: 422 RequestValidationError
        Expected on FIXED code: 200 with [] (test will FAIL after fix)
        """
        response = client.get("/api/available-times/1/abc")
        assert response.status_code == 422, (
            f"Expected 422 (bug condition) but got {response.status_code}. "
            "If this is 200, the bug may already be fixed."
        )

    def test_zero_service_id_current_behavior(self):
        """
        Edge case: service_id=0 is technically a valid integer but not a valid
        positive service ID. On unfixed code, FastAPI accepts it as int and
        proceeds to query the database (no 422 validation error).
        After the fix, 0 should return 200 with [] without DB query.

        This test documents current behavior for service_id=0.
        On unfixed code: 0 is parsed as int, so it does NOT trigger a 422.
        The key assertion is that 0 does NOT get the same 422 as "undefined".
        """
        response = client.get("/api/available-times/1/0")
        # On unfixed code, 0 is parsed as int successfully, so no 422.
        # It passes FastAPI validation (unlike "undefined" or "abc").
        # The endpoint proceeds to the DB layer (may error with mocked DB,
        # but critically it does NOT return 422).
        assert response.status_code != 422, (
            f"service_id=0 should NOT trigger a 422 validation error "
            f"(it's a valid integer), but got {response.status_code}"
        )


class TestPoolConfigurationLimits:
    """
    Bug Condition: The connection pool is configured with oversized values
    (pool_size=15, max_overflow=10, pool_timeout=20) that are too large for
    the Render free-tier PostgreSQL, leading to pool exhaustion under normal load.

    These tests CONFIRM the oversized pool configuration exists by reading
    the actual values from database_postgres.py.
    After the fix, the pool will be reduced (pool_size=5, max_overflow=5,
    pool_timeout=10), causing these tests to FAIL.

    Validates: Requirements 1.1, 1.3, 1.4
    """

    @staticmethod
    def _read_pool_config():
        """Read pool configuration values from database_postgres.py source file."""
        import re

        # Find the database_postgres.py file relative to this test file
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_file_path = os.path.join(project_root, "database_postgres.py")

        with open(db_file_path, "r") as f:
            content = f.read()

        # Parse pool configuration values using regex
        pool_size_match = re.search(r"pool_size\s*=\s*(\d+)", content)
        max_overflow_match = re.search(r"max_overflow\s*=\s*(\d+)", content)
        pool_timeout_match = re.search(r"pool_timeout\s*=\s*(\d+)", content)

        config = {}
        if pool_size_match:
            config["pool_size"] = int(pool_size_match.group(1))
        if max_overflow_match:
            config["max_overflow"] = int(max_overflow_match.group(1))
        if pool_timeout_match:
            config["pool_timeout"] = int(pool_timeout_match.group(1))

        return config

    def test_pool_size_is_oversized(self):
        """
        Bug: pool_size=15 is too large for Render free-tier PostgreSQL.
        Expected on UNFIXED code: pool_size == 15
        Expected on FIXED code: pool_size == 5 (test will FAIL after fix)
        """
        config = self._read_pool_config()
        assert "pool_size" in config, "Could not find pool_size in database_postgres.py"
        assert config["pool_size"] == 15, (
            f"Expected pool_size=15 (oversized bug condition) but got {config['pool_size']}. "
            "If pool_size has been reduced, the bug may already be fixed."
        )

    def test_max_overflow_is_oversized(self):
        """
        Bug: max_overflow=10 combined with pool_size=15 allows up to 25 total
        connections, exhausting the Render free-tier PostgreSQL connection limit.
        Expected on UNFIXED code: max_overflow == 10
        Expected on FIXED code: max_overflow == 5 (test will FAIL after fix)
        """
        config = self._read_pool_config()
        assert "max_overflow" in config, "Could not find max_overflow in database_postgres.py"
        assert config["max_overflow"] == 10, (
            f"Expected max_overflow=10 (oversized bug condition) but got {config['max_overflow']}. "
            "If max_overflow has been reduced, the bug may already be fixed."
        )

    def test_pool_timeout_is_too_long(self):
        """
        Bug: pool_timeout=20 means requests wait up to 20 seconds for a connection
        before failing, causing poor user experience during pool exhaustion.
        Expected on UNFIXED code: pool_timeout == 20
        Expected on FIXED code: pool_timeout == 10 (test will FAIL after fix)
        """
        config = self._read_pool_config()
        assert "pool_timeout" in config, "Could not find pool_timeout in database_postgres.py"
        assert config["pool_timeout"] == 20, (
            f"Expected pool_timeout=20 (too long bug condition) but got {config['pool_timeout']}. "
            "If pool_timeout has been reduced, the bug may already be fixed."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
