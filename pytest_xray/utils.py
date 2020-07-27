import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth
from jira import jira

from .config import (
    JIRA_SERVER,
    XRAY_API,
    JIRA_TECHNICAL_ACCOUNT,
    JIRA_PASSWORD,
    PYTEST_XRAY_MARKER_NAME
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_test_keys = {}
_module_test_execution_mapping = {}

jira = JIRA(options={"server": JIRA_SERVER,
                     "verify": False},
            basic_auth=(JIRA_TECHNICAL_ACCOUNT, JIRA_PASSWORD))

def create_test_execution_per_module(item, test_execution_name):
    if item.parent not in _module_test_execution_mapping.key():
        _module_test_execution_mapping[item.parent] = JiraIssue(
            jira,
            ' '.join([test_execution_name, str(item.parent)]),
            'Test Execution'
        ).issue_key
    return _module_test_execution_mapping[item.parent]

def associate_marker_metadata_for(item, test_execution_key):
    marker = item.get_closest_marker(PYTEST_XRAY_MARKER_NAME)
    if not marker:
        return

    issue_name = marker.kwargs['issue_name']
    test_case_key = JiraIssue(
        jira,
        issue_name,
        'Test'
    ).issue_key

    XrayTestExecution(test_execution_key).add_test(test_case_key)
    _test_keys[item.nodeid] = test_case_key, test_execution_key

class JiraIssue(object):
    def __init__(self, jira, issue_name, issue_type):
        self.jira = jira
        self.issue_name = issue_name
        self.issue_type = issue_type
        self.issue_key = self._set_issue_key()

    def _exists(self):
        return self.jira.search_issues(
            f'project=DAFL and summary~"{self.issue_name}" and issuetype="{self.issue_type}"'
        )

    def _create(self):
        if self.issue_type == "Test Execution":
            return jira.create_issue(
                project='DAFL',
                summary=self.issue_name,
                description='Test',
                issuetype={'name': self.issue_type}
            )
        elif self.issue_type == "Test":
            return jirs.create_issue(
                project='DAFL',
                summary=self.issue_name,
                description='Test',
                issuetype={'name': self.issue_type}
            )
        else:
            raise Exception(
                f"Creation of JIRA issues of type {self.issue_type} not supported"
        )
    
    def _set_issue_key(self):
        issue = self._exists()
        if not issue:
            return self._create().key
        else:
            return issue[0].key

class XrayTestExecution(object):
    def __init__(self, test_execution_key):
        self.test_execution_key = test_execution_key
        self.header = {'Content-Type': 'application/json'}
        self.url = JIRA_SERVER + XRAY_API

    def add_test(self, test_case_key):
        data = {'add': [test_case_key]}

        requests.post(
            self.url + f"/api/testexec/{self.test_execution_key}/test",
            auth=HTTPBasicAuth(JIRA_TECHNICAL_ACCOUNT, JIRA_PASSWORD),
            headers=self.header,
            data=json.dumps(data),
            verify=False
        )
    
    def update_test_result(self, test_case_key, result):
        data = {
            'testExecutionKey': self.test_execution_key,
            'tests': [{'testKey': test_case_key, 'status': result}]
        }

        requests.post(
            self.url + "/import/execution",
            auth=HTTPBasicAuth(JIRA_TECHNICAL_ACCOUNT,JIRA_PASSWORD),
            headers=self.header,
            data=json.dumps(data),
            verify=False
        )