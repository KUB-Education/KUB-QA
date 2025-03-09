import pytest


@pytest.fixture
def headers():
    return {
        "X-SUPER-ADMIN-KEY": "your_super_admin_key_here",
        "Content-Type": "application/json",
    }


@pytest.fixture
def admin_request():
    return {
        "last_name": "Doe",
        "first_name": "John",
        "middle_name": "Edward",
        "email": "john.doe@example.com",
    }


@pytest.fixture
def update_request():
    return {
        "last_name": "Smith",
        "first_name": "Alice",
        "middle_name": "",
        "email": "alice.smith@example.com",
    }
