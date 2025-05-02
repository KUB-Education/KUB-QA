import pytest
from dotenv import load_dotenv
from tavern._core.exceptions import TestFailError

load_dotenv()

#fixtures

@pytest.fixture
def department_setup_description():
    return "When request with valid json body, POST /department returns 201"

@pytest.fixture
def department_cleanup_description():
    return "When department exists, DELETE /department/id returns 204"

@pytest.fixture
def department_cleanup_check_description():
    return "When department deleted, GET /department/id returns 404"

#hooks

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.outcome == "failed":
        if isinstance(call.excinfo.value, TestFailError):
            call.excinfo._excinfo = (AssertionError, AssertionError(str(call.excinfo.value)), call.excinfo.tb)