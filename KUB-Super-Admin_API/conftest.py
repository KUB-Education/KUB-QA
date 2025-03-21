import os

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def headers():
    return {
        "X-SUPER-ADMIN-KEY": os.getenv("TOKEN"),
        "Content-Type": "application/json",
    }


@pytest.fixture
def admin_request():
    return {
        "last_name": "UserLastName",
        "first_name": "UserFirstName",
        "middle_name": "UserMiddleName",
        "email": "UserEmail@example.com",
    }


@pytest.fixture
def update_request():
    return {
        "last_name": "NewUserLastName",
        "first_name": "NewUserFirstName",
        "middle_name": "",
        "email": "NewUserEmail@example.com",
    }