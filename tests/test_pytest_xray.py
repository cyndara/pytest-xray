pytest_plugins = "pytester"

def test_pytest_xray_plugin(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.xray(issue_name="Testing pytest xray plugin for pass")
        def test_function_for_pass:
            assert True

        @pytest.mark.xray(issue_name="Testing pytest xray plugin for fail")
        def test_function_for_fail:
            assert False

        """
    )

    result = testdir.runpytest(
        '-v',
        '--xray',
        '--exec-name=Testing Pytest Xray Plugin'
    )

    expected_lines= [
        "test_pytest_xray_plugin.py::test_function_for_pass ",
        "Test execution: DAFL-*, Test case: DAFL-*",
        "*",
        "test_pytest_xray_plugin.py::test_function_for_fail ",
        "Test execution: DAFL-*, Test case: DAFL-*",
        "*"
    ]

    result.stdout.fmatch_lines(('\n').join(expected_lines))