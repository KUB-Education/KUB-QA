import requests

from .constans import BASE_URL


def create_admin(admin_request, headers):
    """
    Helper function that creates an admin and returns the JSON response.
    """
    response = requests.post(f"{BASE_URL}/admins", json=admin_request, headers=headers)
    assert (
        response.status_code == 201
    ), f"Expected status code 201, got {response.status_code}"
    return response.json()


def remove_admin(headers, admin_id):
    response = requests.delete(f"{BASE_URL}/admins/{admin_id}", headers=headers)
    assert response.status_code == 204, f"Expected 204, got {response.status_code}"
    get_response = requests.get(f"{BASE_URL}/admins/{admin_id}", headers=headers)
    assert (
        get_response.status_code == 404
    ), "After deletion, GET should return 404 Not Found"
