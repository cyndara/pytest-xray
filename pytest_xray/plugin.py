import pytest

from .utils import (
    XrayTestExecution,
    create_test_execution_per_module,
    associate_marker_metadata_for,
    _test_keys
)
from .config import PYTEST_XRAY_MARKER_NAME

JIRA_XRAY_FLAG = "--xray"
XRAY_PLUGIN = "xray"

def pytest_addoption(parser):
    group = parser.getgroup('xray')
    group.addoption(
        "--xray",
        action='store_true',
        help='Create, add and update test cases in JIRA'
    )
    group.addoption(
        "--exec-name"
        dest='EXEC_NAME'
        action='store'
        help='Name of the execution'
    )

def pytest_report_header(config):
    if config.getoption('xray'):
        return "Running tests and JIRA update for test exeuction {}".format(
            config.getoption('EXEC_NAME')
        )

def pytest_report_teststatus(report, config):
    if report.when == 'call':
        if report.passed and config.getoption('xray'):
            return (report.outcome, 'P', 'PASSED')

def pytest_collection_modifyitems(config, items):
    """Created test cases in JIRA for items with xray marker"""
    if config.getoption('xray'):
        for item in items:
            test_execution_key = create_test_execution_per_module(
                item,
                config.getoption('EXEC_NAME')
            )
            associate_marker_metadata_for(item, test_execution_key)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    if (item.config.getoption('EXEC_NAME') and 
    item.get_closest_marker(PYTEST_XRAY_MARKER_NAME)):
        outcome = yield
        result = outcome.get_result()

        if result.when == "call":
            test_case_key = _test_keys[item.nodeid][0]
            test_execution_key = _test_keys[item.nodeid][1]
            print("\nTest execution: {}, Test case: {}".format(
                test_execution_key, test_case_key
            )
            )
            if result.passed:
                XrayTestExecution(test_execution_key).update_test_result(
                    test_case_key,
                    "PASS"
                )
            elif result.failed:
                XrayTestExecution(test_execution_key).update_test_result(
                    test_case_key,
                    "FAIL"
                )
    elif (item.config.getoption('EXEC_NAME') and not
          item.get_closest_marker(PYTEST_XRAY_MARKER_NAME)):
        yield
    else:
        yield