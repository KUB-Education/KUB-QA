import pytest
from dotenv import load_dotenv
from tavern._core.exceptions import TestFailError

load_dotenv()

#hooks

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.outcome == "failed":
        if isinstance(call.excinfo.value, TestFailError):
            call.excinfo._excinfo = (AssertionError, AssertionError(str(call.excinfo.value)), call.excinfo.tb)