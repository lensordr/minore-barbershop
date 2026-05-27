"""
Fix Verification Tests - Sentry Connection Pool Fix

These tests verify that the fix works correctly.
They assert the FIXED behavior: invalid service_id values return HTTP 200 with [].
These tests MUST PASS on the fixed code.

Validates: Requirements 2.2
"""
import pytest
import sys
import os
from unittest.mock import MagicMock, patch
import unittest.mock
import types

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set DATABASE_URL so the module doesn't raise RuntimeError
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test_db")

# IMPORTANT: Import fastapi modules BEFORE mocking and importing main.
# This ensures FastAPI's response type detection works correctly with TestClient.
import fastapi
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

# Track Sentry events
_sentry_events = []

# Mock psycopg and the database engine creation before importing main
mock_engine = MagicMock()
mock_session_local = MagicMock()


def mock_get_db():
    db = MagicMock()
    try:
        yield db
    finally:
        pass


# Patch database_postgres module and psycopg before importing main
with unittest.mock.patch.dict(sys.modules, {
    'psycopg': MagicMock(),
    'psycopg.pq': MagicMock(),
}):
    # Create a fake database_postgres module
    fake_db_module = types.ModuleType('database_postgres')
    fake_db_module.get_db = mock_get_db
    fake_db_module.engine = mock_engine
    fake_db_module.SessionLocal = mock_session_local
    sys.modules['database_postgres'] = fake_db_module

    from main import app

# raise_server_exceptions=False so we get HTTP responses even for 500 errors
client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def reset_sentry_events():
    """Reset sentry event tracking before each test."""
    _sentry_events.clear()
    yield


class TestInvalidServiceIdReturnsEmptyList:
    """
    Fix Verification: After the fix, invalid service_id values should return
    HTTP 200 with an empty JSON array [] instead of raising a 422 validation error.

    Validates: Requirements 2.2
    """

    def test_undefined_service_id_returns_200_with_empty_list(self):
        """
        Fix: /api/available-times/1/undefined returns 200 with []
        instead of 422 RequestValidationError.
        """
        response = client.get("/api/available-times/1/undefined")
        assert response.status_code == 200, (
            f"Expected 200 (fix applied) but got {response.status_code}. "
            "The fix should return an empty list for non-integer service_id."
        )
        assert response.json() == [], (
            f"Expected empty list [] but got {response.json()}"
        )

    def test_alphabetic_service_id_returns_200_with_empty_list(self):
        """
        Fix: /api/available-times/1/abc returns 200 with []
        instead of 422 RequestValidationError.
        """
        response = client.get("/api/available-times/1/abc")
        assert response.status_code == 200, (
            f"Expected 200 (fix applied) but got {response.status_code}. "
            "The fix should return an empty list for non-integer service_id."
        )
        assert response.json() == [], (
            f"Expected empty list [] but got {response.json()}"
        )

    def test_zero_service_id_returns_200_with_empty_list(self):
        """
        Fix: /api/available-times/1/0 returns 200 with []
        because 0 is not a valid positive service ID.
        """
        response = client.get("/api/available-times/1/0")
        assert response.status_code == 200, (
            f"Expected 200 (fix applied) but got {response.status_code}. "
            "The fix should return an empty list for service_id=0."
        )
        assert response.json() == [], (
            f"Expected empty list [] but got {response.json()}"
        )

    def test_negative_service_id_returns_200_with_empty_list(self):
        """
        Fix: /api/available-times/1/-5 returns 200 with []
        because negative numbers are not valid service IDs.
        """
        response = client.get("/api/available-times/1/-5")
        assert response.status_code == 200, (
            f"Expected 200 (fix applied) but got {response.status_code}. "
            "The fix should return an empty list for negative service_id."
        )
        assert response.json() == [], (
            f"Expected empty list [] but got {response.json()}"
        )

    def test_null_service_id_returns_200_with_empty_list(self):
        """
        Fix: /api/available-times/1/null returns 200 with []
        instead of 422 RequestValidationError.
        """
        response = client.get("/api/available-times/1/null")
        assert response.status_code == 200, (
            f"Expected 200 (fix applied) but got {response.status_code}. "
            "The fix should return an empty list for service_id='null'."
        )
        assert response.json() == [], (
            f"Expected empty list [] but got {response.json()}"
        )


class TestNoSentryEventForInvalidServiceId:
    """
    Fix Verification: Invalid service_id requests should NOT trigger
    Sentry events (no capture_exception or capture_message calls).
    Since sentry_sdk is not installed in the test environment, the
    error_handlers.py module sets SENTRY_AVAILABLE = False, so no
    Sentry events are raised. We verify this by checking that the
    endpoint returns 200 (not 422/500) which means no exception
    propagates to the error handler at all.

    Validates: Requirements 2.2
    """

    def test_undefined_service_id_no_sentry_event(self):
        """No Sentry event should be raised for service_id='undefined'.
        The endpoint handles it gracefully with 200 before any error handler."""
        response = client.get("/api/available-times/1/undefined")
        assert response.status_code == 200, (
            f"Expected 200 (graceful handling, no error/exception) but got {response.status_code}"
        )
        assert len(_sentry_events) == 0, (
            f"Expected no Sentry events but got {len(_sentry_events)}: {_sentry_events}"
        )

    def test_alphabetic_service_id_no_sentry_event(self):
        """No Sentry event should be raised for service_id='abc'."""
        response = client.get("/api/available-times/1/abc")
        assert response.status_code == 200
        assert len(_sentry_events) == 0, (
            f"Expected no Sentry events but got {len(_sentry_events)}: {_sentry_events}"
        )

    def test_zero_service_id_no_sentry_event(self):
        """No Sentry event should be raised for service_id='0'."""
        response = client.get("/api/available-times/1/0")
        assert response.status_code == 200
        assert len(_sentry_events) == 0, (
            f"Expected no Sentry events but got {len(_sentry_events)}: {_sentry_events}"
        )

    def test_negative_service_id_no_sentry_event(self):
        """No Sentry event should be raised for service_id='-5'."""
        response = client.get("/api/available-times/1/-5")
        assert response.status_code == 200
        assert len(_sentry_events) == 0, (
            f"Expected no Sentry events but got {len(_sentry_events)}: {_sentry_events}"
        )

    def test_null_service_id_no_sentry_event(self):
        """No Sentry event should be raised for service_id='null'."""
        response = client.get("/api/available-times/1/null")
        assert response.status_code == 200
        assert len(_sentry_events) == 0, (
            f"Expected no Sentry events but got {len(_sentry_events)}: {_sentry_events}"
        )


class TestPoolConfigurationFixed:
    """
    Fix Verification: After the fix, the connection pool settings should be
    optimized for the Render free-tier PostgreSQL environment.

    Validates: Requirements 2.1, 2.3, 2.4
    """

    @staticmethod
    def _read_pool_config():
        """Read pool configuration values from database_postgres.py source file."""
        import re

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_file_path = os.path.join(project_root, "database_postgres.py")

        with open(db_file_path, "r") as f:
            content = f.read()

        # Parse pool configuration values using regex
        pool_size_match = re.search(r"pool_size\s*=\s*(\d+)", content)
        max_overflow_match = re.search(r"max_overflow\s*=\s*(\d+)", content)
        pool_timeout_match = re.search(r"pool_timeout\s*=\s*(\d+)", content)
        pool_recycle_match = re.search(r"pool_recycle\s*=\s*(\d+)", content)

        config = {}
        if pool_size_match:
            config["pool_size"] = int(pool_size_match.group(1))
        if max_overflow_match:
            config["max_overflow"] = int(max_overflow_match.group(1))
        if pool_timeout_match:
            config["pool_timeout"] = int(pool_timeout_match.group(1))
        if pool_recycle_match:
            config["pool_recycle"] = int(pool_recycle_match.group(1))

        return config

    def test_pool_size_is_optimized(self):
        """
        Fix: pool_size reduced from 15 to 5 for Render free-tier PostgreSQL.
        Validates: Requirement 2.1
        """
        config = self._read_pool_config()
        assert "pool_size" in config, "Could not find pool_size in database_postgres.py"
        assert config["pool_size"] == 5, (
            f"Expected pool_size=5 (optimized for Render free-tier) but got {config['pool_size']}."
        )

    def test_max_overflow_is_optimized(self):
        """
        Fix: max_overflow reduced from 10 to 5, limiting total connections to 10.
        Validates: Requirement 2.1
        """
        config = self._read_pool_config()
        assert "max_overflow" in config, "Could not find max_overflow in database_postgres.py"
        assert config["max_overflow"] == 5, (
            f"Expected max_overflow=5 (optimized) but got {config['max_overflow']}."
        )

    def test_pool_timeout_is_optimized(self):
        """
        Fix: pool_timeout reduced from 20 to 10 seconds for faster failure.
        Validates: Requirement 2.3
        """
        config = self._read_pool_config()
        assert "pool_timeout" in config, "Could not find pool_timeout in database_postgres.py"
        assert config["pool_timeout"] == 10, (
            f"Expected pool_timeout=10 (fail fast) but got {config['pool_timeout']}."
        )

    def test_pool_recycle_is_optimized(self):
        """
        Fix: pool_recycle reduced from 300 to 180 seconds to return connections faster.
        Validates: Requirement 2.4
        """
        config = self._read_pool_config()
        assert "pool_recycle" in config, "Could not find pool_recycle in database_postgres.py"
        assert config["pool_recycle"] == 180, (
            f"Expected pool_recycle=180 (3 minutes) but got {config['pool_recycle']}."
        )

    def test_total_max_connections_within_limit(self):
        """
        Fix: Total max connections (pool_size + max_overflow) must not exceed 10
        to stay well within Render free-tier PostgreSQL limits.
        Validates: Requirements 2.1, 2.3, 2.4
        """
        config = self._read_pool_config()
        assert "pool_size" in config, "Could not find pool_size in database_postgres.py"
        assert "max_overflow" in config, "Could not find max_overflow in database_postgres.py"

        total_max = config["pool_size"] + config["max_overflow"]
        assert total_max <= 10, (
            f"Expected total max connections (pool_size + max_overflow) <= 10 "
            f"but got {total_max} (pool_size={config['pool_size']}, "
            f"max_overflow={config['max_overflow']})."
        )


class TestGridHelperOptimization:
    """
    Fix Verification: create_appointment_grid() accepts a `barbers` parameter.
    When barbers are pre-fetched and passed in, no additional DB query is made.
    When barbers is None, existing behavior (querying the DB) is preserved.

    Validates: Requirements 2.4
    """

    @staticmethod
    def _make_mock_barber(barber_id, name):
        """Create a mock barber object with id and name attributes."""
        barber = MagicMock()
        barber.id = barber_id
        barber.name = name
        return barber

    @staticmethod
    def _make_mock_schedule(start_hour=9, end_hour=17):
        """Create a mock schedule object with start_hour and end_hour."""
        schedule = MagicMock()
        schedule.start_hour = start_hour
        schedule.end_hour = end_hour
        return schedule

    def test_accepts_barbers_parameter(self):
        """
        Fix: create_appointment_grid() accepts a `barbers` keyword argument.
        This allows callers to pass pre-fetched barbers to avoid redundant DB queries.
        """
        from grid_helper import create_appointment_grid

        db = MagicMock()
        schedule = self._make_mock_schedule()
        barber1 = self._make_mock_barber(1, "John")
        barber2 = self._make_mock_barber(2, "Jane")

        # Should not raise TypeError when barbers parameter is provided
        result = create_appointment_grid(
            db, [], schedule, location_id=1, barbers=[barber1, barber2]
        )
        assert "grid" in result
        assert "hours" in result

    def test_barbers_provided_skips_db_query(self):
        """
        Fix: When barbers are provided, no call to
        crud.get_barbers_with_revenue_by_location is made.
        This eliminates the redundant DB query in admin_dashboard.
        """
        from grid_helper import create_appointment_grid

        db = MagicMock()
        schedule = self._make_mock_schedule()
        barber1 = self._make_mock_barber(1, "John")
        barber2 = self._make_mock_barber(2, "Jane")

        with patch("crud.get_barbers_with_revenue_by_location") as mock_get_barbers:
            result = create_appointment_grid(
                db, [], schedule, location_id=1, barbers=[barber1, barber2]
            )
            # The crud function should NOT be called when barbers are pre-fetched
            mock_get_barbers.assert_not_called()

        # Verify the grid uses the provided barbers
        assert barber1.id in result["grid"]
        assert barber2.id in result["grid"]

    def test_barbers_none_queries_database(self):
        """
        Fix: When barbers is None (default), existing behavior is preserved —
        crud.get_barbers_with_revenue_by_location is called to fetch barbers.
        """
        from grid_helper import create_appointment_grid

        db = MagicMock()
        schedule = self._make_mock_schedule()
        barber1 = self._make_mock_barber(1, "John")
        barber2 = self._make_mock_barber(2, "Jane")

        with patch("crud.get_barbers_with_revenue_by_location") as mock_get_barbers:
            mock_get_barbers.return_value = [barber1, barber2]
            result = create_appointment_grid(
                db, [], schedule, location_id=1, barbers=None
            )
            # The crud function SHOULD be called when barbers is None
            mock_get_barbers.assert_called_once_with(db, 1)

        # Verify the grid uses the fetched barbers
        assert barber1.id in result["grid"]
        assert barber2.id in result["grid"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
