Description
====

This pytest plugin help reduce the manual overhead of creating test execution
issues in JIRA, as well as the manual linking of test cases to test executions 
and updating of test case results, especially if the tests are automated. With
this plugin, creation of a test execution issue, linking of test cases to the 
execution and test states are automatically updated as the tests run.


Terminology
====

* test execution - test execution issue in JIRA
* test case - test issue in JIRA
* test status - result of the test case (PASS or FAIL)

Plugin installation
====

To install this library for use please execute the following:

    $ pip install pytest-xray

How to use
====

Integration tests for user stories in JIRA should be decorated as below

    @pytest.mark.xray(summary="Testing function foo")
    def test_foo():
        assert True == True

The summary argument for the decorator specifies the name that the test case
should have in JIRA.

Enable the plugin by passing the extra options --xray and --exec-name to the
command line when invoking the pytest runner:

    $ pytest . --xray --exec-name=$EXECUTION_NAME

A test execution is created in JIRA per test module found, the argument
$EXECUTION_NAME is prepended to all test executions that are created during the
test run.

It is important that the variables **JIRA_TECHNICAL_ACCOUNT** and
**JIRA_PASSWORD** are set in the environment for pytest-xray to successfully
make API requests to JIRA and Xray.
