"""
Preservation Tests - Sentry Connection Pool Fix

These tests verify that existing functionality is preserved after the fix.
They ensure no regressions were introduced by the pool configuration changes
and service_id validation additions.

Validates: Requirements 3.1, 3.4
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
import fastapi
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

# Mock psycopg and the database engine creation before importing main
mock_engine = MagicMock()
mock_session_local = MagicMock()

# We'll store a reference to the mock db so tests can configure it
_mock_db = MagicMock()


def mock_get_db():
    try:
        yield _mock_db
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

    from main import app, check_admin_auth
    import crud as _crud_module
    import main as _main_module

# Re-register modules in sys.modules so patch("crud.xxx") can find them
sys.modules['crud'] = _crud_module
sys.modules['main'] = _main_module

# Keep 'crud' name available for existing tests
crud = _crud_module

# raise_server_exceptions=False so we get HTTP responses even for 500 errors
client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def reset_mock_db():
    """Reset the mock db before each test so query chains are fresh."""
    global _mock_db
    _mock_db.reset_mock()
    yield


class TestValidServiceIdReturnsTimesList:
    """
    Preservation: Valid integer service_id values (1, 2, 3, etc.) should
    return HTTP 200 with a JSON list of time strings. The fix must NOT
    break the existing behavior for valid requests.

    Validates: Requirements 3.1
    """

    @pytest.fixture(autouse=True)
    def mock_crud_functions(self):
        """Mock the crud functions that the endpoint calls for valid requests."""
        mock_barber = MagicMock()
        mock_barber.id = 1
        mock_barber.name = "John"
        mock_barber.active = True
        mock_barber.early_access_enabled = False

        mock_schedule = MagicMock()
        mock_schedule.start_hour = 9
        mock_schedule.end_hour = 17
        mock_schedule.is_open = True

        sample_times = ["10:00", "10:30", "11:00", "11:30", "12:00"]

        self.mock_get_barber = MagicMock(return_value=mock_barber)
        self.mock_get_schedule = MagicMock(return_value=mock_schedule)
        self.mock_get_times = MagicMock(return_value=sample_times)

        original_get_barber = crud.get_barber_by_id
        original_get_schedule = crud.get_schedule
        original_get_times = crud.get_available_times_for_service

        crud.get_barber_by_id = self.mock_get_barber
        crud.get_schedule = self.mock_get_schedule
        crud.get_available_times_for_service = self.mock_get_times

        yield

        crud.get_barber_by_id = original_get_barber
        crud.get_schedule = original_get_schedule
        crud.get_available_times_for_service = original_get_times

    def test_service_id_1_returns_200_with_list(self):
        """Valid service_id=1 returns HTTP 200 with a list of time strings."""
        response = client.get("/api/available-times/1/1")
        assert response.status_code == 200, (
            f"Expected 200 for valid service_id=1 but got {response.status_code}"
        )
        data = response.json()
        assert isinstance(data, list), (
            f"Expected a list response but got {type(data).__name__}: {data}"
        )

    def test_service_id_2_returns_200_with_list(self):
        """Valid service_id=2 returns HTTP 200 with a list of time strings."""
        response = client.get("/api/available-times/1/2")
        assert response.status_code == 200, (
            f"Expected 200 for valid service_id=2 but got {response.status_code}"
        )
        data = response.json()
        assert isinstance(data, list), (
            f"Expected a list response but got {type(data).__name__}: {data}"
        )

    def test_service_id_3_returns_200_with_list(self):
        """Valid service_id=3 returns HTTP 200 with a list of time strings."""
        response = client.get("/api/available-times/1/3")
        assert response.status_code == 200, (
            f"Expected 200 for valid service_id=3 but got {response.status_code}"
        )
        data = response.json()
        assert isinstance(data, list), (
            f"Expected a list response but got {type(data).__name__}: {data}"
        )

    def test_service_id_10_returns_200_with_list(self):
        """Valid service_id=10 returns HTTP 200 with a list of time strings."""
        response = client.get("/api/available-times/1/10")
        assert response.status_code == 200, (
            f"Expected 200 for valid service_id=10 but got {response.status_code}"
        )
        data = response.json()
        assert isinstance(data, list), (
            f"Expected a list response but got {type(data).__name__}: {data}"
        )

    def test_valid_service_id_does_not_return_422(self):
        """Valid integer service_ids must NOT return 422 validation error."""
        for service_id in [1, 2, 3, 5, 10]:
            response = client.get(f"/api/available-times/1/{service_id}")
            assert response.status_code != 422, (
                f"service_id={service_id} returned 422 validation error. "
                "Valid integer service_ids should be accepted."
            )

    def test_response_contains_time_strings(self):
        """Valid request returns a list containing time strings (HH:MM format)."""
        response = client.get("/api/available-times/1/1")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # The mocked response should contain time strings
        for time_str in data:
            assert isinstance(time_str, str), (
                f"Expected time string but got {type(time_str).__name__}: {time_str}"
            )
            # Verify time format (HH:MM)
            assert ":" in time_str, (
                f"Expected time in HH:MM format but got: {time_str}"
            )

    def test_valid_service_id_calls_crud_functions(self):
        """Valid service_id triggers the expected crud function calls."""
        response = client.get("/api/available-times/1/1")
        assert response.status_code == 200
        # Verify crud.get_barber_by_id was called with the barber_id
        self.mock_get_barber.assert_called()
        # Verify crud.get_schedule was called
        self.mock_get_schedule.assert_called()
        # Verify crud.get_available_times_for_service was called
        self.mock_get_times.assert_called()


class TestValidServiceIdWithDifferentBarbers:
    """
    Preservation: Valid requests with different barber_id values should
    all return HTTP 200 with a JSON list.

    Validates: Requirements 3.1
    """

    @pytest.fixture(autouse=True)
    def mock_crud_functions(self):
        """Mock the crud functions for valid barber requests."""
        mock_barber = MagicMock()
        mock_barber.id = 2
        mock_barber.name = "Jane"
        mock_barber.active = True
        mock_barber.early_access_enabled = False

        mock_schedule = MagicMock()
        mock_schedule.start_hour = 9
        mock_schedule.end_hour = 17
        mock_schedule.is_open = True

        sample_times = ["09:00", "09:30", "10:00"]

        original_get_barber = crud.get_barber_by_id
        original_get_schedule = crud.get_schedule
        original_get_times = crud.get_available_times_for_service

        crud.get_barber_by_id = MagicMock(return_value=mock_barber)
        crud.get_schedule = MagicMock(return_value=mock_schedule)
        crud.get_available_times_for_service = MagicMock(return_value=sample_times)

        yield

        crud.get_barber_by_id = original_get_barber
        crud.get_schedule = original_get_schedule
        crud.get_available_times_for_service = original_get_times

    def test_barber_2_service_1_returns_200(self):
        """Valid request with barber_id=2, service_id=1 returns 200."""
        response = client.get("/api/available-times/2/1")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_barber_3_service_2_returns_200(self):
        """Valid request with barber_id=3, service_id=2 returns 200."""
        response = client.get("/api/available-times/3/2")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_barber_1_service_3_returns_200(self):
        """Valid request with barber_id=1, service_id=3 returns 200."""
        response = client.get("/api/available-times/1/3")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestValidServiceIdEmptyTimesResponse:
    """
    Preservation: When a valid service_id is provided but no times are
    available (e.g., fully booked), the endpoint should still return
    HTTP 200 with an empty list [].

    Validates: Requirements 3.1
    """

    @pytest.fixture(autouse=True)
    def mock_crud_functions(self):
        """Mock crud functions returning empty times list."""
        mock_barber = MagicMock()
        mock_barber.id = 1
        mock_barber.name = "John"
        mock_barber.active = True
        mock_barber.early_access_enabled = False

        mock_schedule = MagicMock()
        mock_schedule.start_hour = 9
        mock_schedule.end_hour = 17
        mock_schedule.is_open = True

        # No available times (fully booked)
        empty_times = []

        original_get_barber = crud.get_barber_by_id
        original_get_schedule = crud.get_schedule
        original_get_times = crud.get_available_times_for_service

        crud.get_barber_by_id = MagicMock(return_value=mock_barber)
        crud.get_schedule = MagicMock(return_value=mock_schedule)
        crud.get_available_times_for_service = MagicMock(return_value=empty_times)

        yield

        crud.get_barber_by_id = original_get_barber
        crud.get_schedule = original_get_schedule
        crud.get_available_times_for_service = original_get_times

    def test_valid_service_id_no_times_returns_200_empty_list(self):
        """Valid service_id with no available times returns 200 with []."""
        response = client.get("/api/available-times/1/1")
        assert response.status_code == 200, (
            f"Expected 200 even when no times available, got {response.status_code}"
        )
        assert response.json() == [], (
            f"Expected empty list when no times available, got {response.json()}"
        )

    def test_valid_service_id_2_no_times_returns_200_empty_list(self):
        """Valid service_id=2 with no available times returns 200 with []."""
        response = client.get("/api/available-times/1/2")
        assert response.status_code == 200
        assert response.json() == []

    def test_valid_service_id_3_no_times_returns_200_empty_list(self):
        """Valid service_id=3 with no available times returns 200 with []."""
        response = client.get("/api/available-times/1/3")
        assert response.status_code == 200
        assert response.json() == []


class TestAdminDashboardPreservation:
    """
    Preservation Tests: Verify that the admin dashboard continues to work
    correctly after the connection pool fix and grid_helper optimization.

    - Unauthenticated requests should redirect to login
    - Authenticated requests should return HTTP 200 with correct template rendering
    - The appointment grid should be generated correctly with pre-fetched barbers

    Validates: Requirements 3.3
    """

    def _make_mock_barber(self, barber_id, name, active=True):
        """Create a mock barber object."""
        barber = MagicMock()
        barber.id = barber_id
        barber.name = name
        barber.active = active
        barber.location_id = 1
        return barber

    def _make_mock_service(self, service_id, name, duration=30):
        """Create a mock service object."""
        service = MagicMock()
        service.id = service_id
        service.name = name
        service.duration = duration
        service.location_id = 1
        return service

    def _make_mock_schedule(self, start_hour=9, end_hour=17):
        """Create a mock schedule object."""
        schedule = MagicMock()
        schedule.start_hour = start_hour
        schedule.end_hour = end_hour
        return schedule

    def _make_mock_counts(self, total=5, completed=2, cancelled=1):
        """Create a mock counts object."""
        counts = MagicMock()
        counts.total = total
        counts.completed = completed
        counts.cancelled = cancelled
        return counts

    def _patch_all_crud(self, barbers, services, schedule, counts, appointments=None):
        """Create a context manager that patches all crud functions used by admin_dashboard.
        
        We patch on the crud module from sys.modules to ensure the patches
        intercept calls made from within the admin_dashboard endpoint.
        """
        appointments = appointments or []
        active_barbers = [b for b in barbers if b.active]

        return unittest.mock.patch.multiple(
            _crud_module,
            get_appointments_by_date_and_location=MagicMock(return_value=appointments),
            get_barbers_with_revenue_by_location=MagicMock(return_value=barbers),
            get_services_by_location=MagicMock(return_value=services),
            get_schedule=MagicMock(return_value=schedule),
            get_appointment_counts_by_date_and_location=MagicMock(return_value=counts),
            get_active_barbers_by_location=MagicMock(return_value=active_barbers),
        )

    def test_unauthenticated_check_returns_redirect(self):
        """
        Preservation: The check_admin_auth dependency should return a
        RedirectResponse to /admin/login when the cookie is missing.
        """
        from starlette.responses import RedirectResponse as StarletteRedirect

        # Call the auth check directly with no cookie
        result = check_admin_auth(request=MagicMock(), admin_logged_in=None)
        assert isinstance(result, StarletteRedirect), (
            f"Expected RedirectResponse for unauthenticated request but got {type(result)}"
        )
        assert result.status_code == 303, (
            f"Expected 303 status code but got {result.status_code}"
        )
        # Check the location header
        assert result.headers.get("location") == "/admin/login", (
            f"Expected redirect to /admin/login but got {result.headers.get('location')}"
        )

    def test_authenticated_request_returns_200(self):
        """
        Preservation: Authenticated requests to /admin/dashboard should
        return HTTP 200 with HTML content.
        """
        barber1 = self._make_mock_barber(1, "John")
        barber2 = self._make_mock_barber(2, "Jane")
        service1 = self._make_mock_service(1, "Haircut", 30)
        schedule = self._make_mock_schedule()
        counts = self._make_mock_counts()

        with self._patch_all_crud([barber1, barber2], [service1], schedule, counts):
            response = client.get(
                "/admin/dashboard",
                cookies={"admin_logged_in": "true"},
                follow_redirects=False,
            )

        assert response.status_code == 200, (
            f"Expected 200 for authenticated admin dashboard but got {response.status_code}"
        )
        assert "text/html" in response.headers.get("content-type", ""), (
            "Expected HTML content type for admin dashboard response"
        )

    def test_authenticated_dashboard_contains_barber_names(self):
        """
        Preservation: The admin dashboard should display barber names
        in the rendered HTML.
        """
        barber1 = self._make_mock_barber(1, "John")
        barber2 = self._make_mock_barber(2, "Jane")
        service1 = self._make_mock_service(1, "Haircut", 30)
        schedule = self._make_mock_schedule()
        counts = self._make_mock_counts()

        with self._patch_all_crud([barber1, barber2], [service1], schedule, counts):
            response = client.get(
                "/admin/dashboard",
                cookies={"admin_logged_in": "true"},
                follow_redirects=False,
            )

        assert response.status_code == 200
        html_content = response.text
        assert "John" in html_content, (
            "Expected barber name 'John' in dashboard HTML"
        )
        assert "Jane" in html_content, (
            "Expected barber name 'Jane' in dashboard HTML"
        )

    def test_authenticated_dashboard_contains_appointment_grid(self):
        """
        Preservation: The admin dashboard should render the appointment grid
        with time slots generated from the schedule.
        """
        barber1 = self._make_mock_barber(1, "John")
        service1 = self._make_mock_service(1, "Haircut", 30)
        schedule = self._make_mock_schedule(start_hour=9, end_hour=17)
        counts = self._make_mock_counts()

        with self._patch_all_crud([barber1], [service1], schedule, counts):
            response = client.get(
                "/admin/dashboard",
                cookies={"admin_logged_in": "true"},
                follow_redirects=False,
            )

        assert response.status_code == 200
        html_content = response.text
        # The grid should contain time slots from the schedule (09:00 to 16:30)
        assert "09:00" in html_content, (
            "Expected time slot '09:00' in appointment grid"
        )
        assert "12:00" in html_content, (
            "Expected time slot '12:00' in appointment grid"
        )
        assert "16:30" in html_content, (
            "Expected time slot '16:30' in appointment grid"
        )

    def test_grid_generated_with_prefetched_barbers(self):
        """
        Preservation: The appointment grid should be generated correctly
        using pre-fetched barbers (optimization from task 2.3/2.4).
        The grid_helper should NOT make an additional DB query for barbers
        when they are passed from the dashboard handler.
        """
        barber1 = self._make_mock_barber(1, "John")
        barber2 = self._make_mock_barber(2, "Jane")
        service1 = self._make_mock_service(1, "Haircut", 30)
        schedule = self._make_mock_schedule()
        counts = self._make_mock_counts()

        mock_get_barbers = MagicMock(return_value=[barber1, barber2])
        with unittest.mock.patch.multiple(
            _crud_module,
            get_appointments_by_date_and_location=MagicMock(return_value=[]),
            get_barbers_with_revenue_by_location=mock_get_barbers,
            get_services_by_location=MagicMock(return_value=[service1]),
            get_schedule=MagicMock(return_value=schedule),
            get_appointment_counts_by_date_and_location=MagicMock(return_value=counts),
            get_active_barbers_by_location=MagicMock(return_value=[barber1, barber2]),
        ):
            response = client.get(
                "/admin/dashboard",
                cookies={"admin_logged_in": "true"},
                follow_redirects=False,
            )

            # The barbers query should be called exactly once (from the dashboard handler)
            # NOT twice (which would happen if grid_helper also queried for barbers)
            mock_get_barbers.assert_called_once()

        assert response.status_code == 200

    def test_dashboard_displays_appointment_stats(self):
        """
        Preservation: The admin dashboard should display appointment statistics
        (total, completed, cancelled counts).
        """
        barber1 = self._make_mock_barber(1, "John")
        service1 = self._make_mock_service(1, "Haircut", 30)
        schedule = self._make_mock_schedule()
        counts = self._make_mock_counts(total=8, completed=3, cancelled=2)

        with self._patch_all_crud([barber1], [service1], schedule, counts):
            response = client.get(
                "/admin/dashboard",
                cookies={"admin_logged_in": "true"},
                follow_redirects=False,
            )

        assert response.status_code == 200
        html_content = response.text
        # The template renders counts.total, counts.completed, counts.cancelled
        assert "8" in html_content, "Expected total count '8' in dashboard stats"
        assert "3" in html_content, "Expected completed count '3' in dashboard stats"
        assert "2" in html_content, "Expected cancelled count '2' in dashboard stats"


class TestAppointmentDetailsPreservation:
    """
    Preservation: The /api/appointment-details/{appointment_id} endpoint
    must continue to return correct phone, email, and service_id fields
    after the connection pool fix.

    Validates: Requirements 3.4
    """

    def _make_mock_appointment(self, phone="0612345678", email="client@example.com", service_id=2):
        """Create a mock appointment object with phone, email, and service_id."""
        appointment = MagicMock()
        appointment.phone = phone
        appointment.email = email
        appointment.service_id = service_id
        return appointment

    def test_valid_appointment_returns_200_with_details(self):
        """
        Preservation: /api/appointment-details/{valid_id} returns HTTP 200
        with JSON containing phone, email, and service_id fields.
        """
        mock_appointment = self._make_mock_appointment(
            phone="0698765432", email="john@barbershop.com", service_id=3
        )
        _mock_db.query.return_value.filter.return_value.first.return_value = mock_appointment

        response = client.get("/api/appointment-details/1")

        assert response.status_code == 200, (
            f"Expected HTTP 200 but got {response.status_code}"
        )
        data = response.json()
        assert data["phone"] == "0698765432", (
            f"Expected phone='0698765432' but got '{data.get('phone')}'"
        )
        assert data["email"] == "john@barbershop.com", (
            f"Expected email='john@barbershop.com' but got '{data.get('email')}'"
        )
        assert data["service_id"] == 3, (
            f"Expected service_id=3 but got {data.get('service_id')}"
        )

    def test_appointment_details_accepts_integer_id(self):
        """
        Preservation: The endpoint accepts integer appointment_id values
        without raising validation errors.
        """
        mock_appointment = self._make_mock_appointment(
            phone="0611111111", email="test@test.com", service_id=1
        )
        _mock_db.query.return_value.filter.return_value.first.return_value = mock_appointment

        # Test with various valid integer IDs
        for appointment_id in [1, 5, 100, 9999]:
            response = client.get(f"/api/appointment-details/{appointment_id}")
            assert response.status_code == 200, (
                f"Expected HTTP 200 for appointment_id={appointment_id} "
                f"but got {response.status_code}"
            )

    def test_appointment_details_returns_correct_structure(self):
        """
        Preservation: The response JSON always contains phone, email,
        and service_id keys with correct types.
        """
        mock_appointment = self._make_mock_appointment(
            phone="0644556677", email="maria@example.com", service_id=5
        )
        _mock_db.query.return_value.filter.return_value.first.return_value = mock_appointment

        response = client.get("/api/appointment-details/42")

        assert response.status_code == 200
        data = response.json()

        # Verify all expected keys are present
        assert "phone" in data, "Response missing 'phone' field"
        assert "email" in data, "Response missing 'email' field"
        assert "service_id" in data, "Response missing 'service_id' field"

        # Verify types
        assert isinstance(data["phone"], str), (
            f"Expected phone to be str but got {type(data['phone'])}"
        )
        assert isinstance(data["email"], str), (
            f"Expected email to be str but got {type(data['email'])}"
        )
        assert isinstance(data["service_id"], int), (
            f"Expected service_id to be int but got {type(data['service_id'])}"
        )

    def test_appointment_details_with_realistic_data(self):
        """
        Preservation: The endpoint correctly returns realistic appointment
        data including phone numbers, emails, and service IDs as stored.
        """
        test_cases = [
            {"phone": "+34612345678", "email": "cliente@gmail.com", "service_id": 1},
            {"phone": "0699887766", "email": "vip@barbershop.es", "service_id": 4},
            {"phone": "", "email": "nophone@test.com", "service_id": 2},
        ]

        for case in test_cases:
            mock_appointment = self._make_mock_appointment(**case)
            _mock_db.query.return_value.filter.return_value.first.return_value = mock_appointment

            response = client.get("/api/appointment-details/10")

            assert response.status_code == 200
            data = response.json()
            assert data["phone"] == case["phone"], (
                f"Expected phone='{case['phone']}' but got '{data['phone']}'"
            )
            assert data["email"] == case["email"], (
                f"Expected email='{case['email']}' but got '{data['email']}'"
            )
            assert data["service_id"] == case["service_id"], (
                f"Expected service_id={case['service_id']} but got {data['service_id']}"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
