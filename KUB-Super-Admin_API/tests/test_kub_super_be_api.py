import requests

from .constans import BASE_URL
from .helper import create_admin


# ----------------- POST /admins -----------------
def test_create_admin_success(admin, admin_request, headers):
    """
    Test POST /admins returns 201 Created when a valid admin is provided.
    """
    assert "id" in admin, "Response should contain 'id'"
    assert (
        admin["email"] == admin_request["email"]
    ), "Email should match the request data"


def test_create_admin_bad_request(headers):
    """
    Test POST /admins returns 400 Bad Request when required fields are missing.
    """
    invalid_request = {
        "last_name": "Doe",
        "middle_name": "Edward",
        "email": "john.doe@example.com",
    }
    response = requests.post(
        f"{BASE_URL}/admins", json=invalid_request, headers=headers
    )
    data = response.json()
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    assert "firstName can't be blank" in data["detail"]


def test_create_admin_unauthorized(admin_request):
    """
    Test POST /admins returns 401 Unauthorized when the header is missing.
    """
    response = requests.post(f"{BASE_URL}/admins", json=admin_request)
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"


def test_create_admin_conflict(admin, admin_request, headers):
    """
    Test POST /admins returns 409 Conflict when an admin with the same email already exists.
    """
    response = requests.post(f"{BASE_URL}/admins", json=admin_request, headers=headers)
    data = response.json()
    assert response.status_code == 409, f"Expected 409, got {response.status_code}"
    assert data["detail"] == "User exists"


def test_create_admin_unprocessable_entity(headers):
    """
    Test POST /admins returns 422 Unprocessable Entity when validation fails.
    """
    invalid_request = {
        "last_name": "Doe",
        "first_name": "John123",
        "middle_name": "Edward",
        "email": "invalid-email",
    }
    response = requests.post(
        f"{BASE_URL}/admins", json=invalid_request, headers=headers
    )
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


# ----------------- GET /admins -----------------
def test_get_admins_success(admin, headers):
    """
    Test GET /admins returns 200 OK and a list of admins.
    """
    response = requests.get(f"{BASE_URL}/admins", headers=headers)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Response should be a list"


def test_get_admins_unauthorized():
    """
    Test GET /admins returns 401 Unauthorized when the header is missing.
    """
    response = requests.get(f"{BASE_URL}/admins")
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"


# ----------------- GET /admins/{id} -----------------
def test_get_admin_by_id_success(admin, headers):
    """
    Test GET /admins/{id} returns 200 OK for a valid admin.
    """
    admin_id = admin["id"]
    response = requests.get(f"{BASE_URL}/admins/{admin_id}", headers=headers)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["id"] == admin_id, "Returned id should match"


def test_get_admin_by_id_bad_request(headers):
    """
    Test GET /admins/{id} returns 400 Bad Request when id is not an integer.
    """
    response = requests.get(f"{BASE_URL}/admins/abc", headers=headers)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


def test_get_admin_by_id_unauthorized(admin, headers):
    """
    Test GET /admins/{id} returns 401 Unauthorized when the header is missing.
    """
    admin_id = admin["id"]
    response = requests.get(f"{BASE_URL}/admins/{admin_id}")
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"


def test_get_admin_by_id_unprocessable_entity(headers):
    """
    Test GET /admins/{id} returns 422 Unprocessable Entity when id fails validation (e.g., negative id).
    """
    response = requests.get(f"{BASE_URL}/admins/-1", headers=headers)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


def test_get_admin_by_id_not_found(headers):
    """
    Test GET /admins/{id} returns 404 Not Found for a non-existent admin.
    """
    response = requests.get(f"{BASE_URL}/admins/999999", headers=headers)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


# ----------------- PUT /admins/{id} -----------------
def test_update_admin_success(admin, update_request, headers):
    """
    Test PUT /admins/{id} returns 200 OK when updating an existing admin.
    """
    admin_id = admin["id"]
    response = requests.put(
        f"{BASE_URL}/admins/{admin_id}", json=update_request, headers=headers
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert (
        data["last_name"] == update_request["last_name"]
    ), "Last name should be updated"


def test_update_admin_bad_request(admin, headers):
    """
    Test PUT /admins/{id} returns 400 Bad Request when the payload is invalid.
    """
    admin_id = admin["id"]
    invalid_update = {
        "last_name": "Smith",
        "first_name": "Alice",
        "middle_name": "",
        "email": 12345,
    }
    response = requests.put(
        f"{BASE_URL}/admins/{admin_id}", json=invalid_update, headers=headers
    )
    data = response.json()
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    assert "email must be a valid email address" in data["detail"]
    assert "middleName must have length in interval" in data["detail"]


def test_update_admin_unauthorized(admin, update_request):
    """
    Test PUT /admins/{id} returns 401 Unauthorized when the header is missing.
    """
    headers_invalid = {
        "Content-Type": "application/json",
        "X-SUPER-ADMIN-KEY": "your_super_admin_key_here",
    }
    admin_id = admin["id"]
    response = requests.put(
        f"{BASE_URL}/admins/{admin_id}", json=update_request, headers=headers_invalid
    )
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"


def test_update_admin_unprocessable_entity(admin, headers):
    """
    Test PUT /admins/{id} returns 422 Unprocessable Entity when validation fails.
    """
    admin_id = admin["id"]
    invalid_update = {
        "last_name": "Smith",
        "first_name": "Alice123",
        "middle_name": "",
        "email": "alice.smith@example.com",
    }
    response = requests.put(
        f"{BASE_URL}/admins/{admin_id}", json=invalid_update, headers=headers
    )
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


def test_update_admin_not_found(update_request, headers):
    """
    Test PUT /admins/{id} returns 404 Not Found when updating a non-existent admin.
    """
    response = requests.put(
        f"{BASE_URL}/admins/999999", json=update_request, headers=headers
    )
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


# ----------------- DELETE /admins/{id} -----------------
def test_delete_admin_success(admin_request, headers):
    """
    Test DELETE /admins/{id} returns 204 No Content when deletion is successful.
    """
    created_admin = create_admin(admin_request, headers)
    admin_id = created_admin["id"]
    response = requests.delete(f"{BASE_URL}/admins/{admin_id}", headers=headers)
    assert response.status_code == 204, f"Expected 204, got {response.status_code}"
    get_response = requests.get(f"{BASE_URL}/admins/{admin_id}", headers=headers)
    assert (
        get_response.status_code == 404
    ), "After deletion, GET should return 404 Not Found"


def test_delete_admin_bad_request(headers):
    """
    Test DELETE /admins/{id} returns 400 Bad Request when id is not an integer.
    """
    response = requests.delete(f"{BASE_URL}/admins/abc", headers=headers)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


def test_delete_admin_unauthorized(admin):
    """
    Test DELETE /admins/{id} returns 401 Unauthorized when the header is missing.
    """
    headers_valid = {
        "Content-Type": "application/json",
        "X-SUPER-ADMIN-KEY": "your_super_admin_key_here",
    }
    admin_id = admin["id"]
    response = requests.delete(f"{BASE_URL}/admins/{admin_id}", headers=headers_valid)
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"


def test_delete_admin_unprocessable_entity(headers):
    """
    Test DELETE /admins/{id} returns 422 Unprocessable Entity when id fails validation.
    """
    response = requests.delete(f"{BASE_URL}/admins/-1", headers=headers)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


def test_delete_admin_not_found(headers):
    """
    Test DELETE /admins/{id} returns 404 Not Found for a non-existent admin.
    """
    response = requests.delete(f"{BASE_URL}/admins/999999", headers=headers)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


# ----------------- POST /admins/{id}/resend -----------------
def test_resend_admin_success(admin, headers):
    """
    Test POST /admins/{id}/resend returns 200 OK (or 503 for SMTP failure) for a valid admin.
    """
    admin_id = admin["id"]
    response = requests.post(f"{BASE_URL}/admins/{admin_id}/resend", headers=headers)
    assert response.status_code in [
        200,
        503,
    ], f"Expected 200 or 503, got {response.status_code}"
    if response.status_code == 200:
        data = response.json()
        assert data["id"] == admin_id, "Returned admin id should match"


def test_resend_admin_bad_request(headers):
    """
    Test POST /admins/{id}/resend returns 400 Bad Request when id is not an integer.
    """
    response = requests.post(f"{BASE_URL}/admins/abc/resend", headers=headers)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"


def test_resend_admin_unauthorized(admin):
    """
    Test POST /admins/{id}/resend returns 401 Unauthorized when the header is missing.
    """
    headers_valid = {
        "Content-Type": "application/json",
        "X-SUPER-ADMIN-KEY": "your_super_admin_key_here",
    }
    admin_id = admin["id"]
    response = requests.post(
        f"{BASE_URL}/admins/{admin_id}/resend", headers=headers_valid
    )
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"


def test_resend_admin_unprocessable_entity(headers):
    """
    Test POST /admins/{id}/resend returns 422 Unprocessable Entity when id fails validation.
    """
    response = requests.post(f"{BASE_URL}/admins/-1/resend", headers=headers)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"


def test_resend_admin_not_found(headers):
    """
    Test POST /admins/{id}/resend returns 404 Not Found for a non-existent admin.
    """
    response = requests.post(f"{BASE_URL}/admins/999999/resend", headers=headers)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
