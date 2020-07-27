from setuptools import setup

REQUIRED_PACKAGES = [
    'pytest==4.3.1',
    'jira==2.0.0',
    'requests==2.21.0',
    'urllib3==1.42.3'
]

setup(
    name='pytest-xray',
    version='0.0.1',
    description="""Plugin for automatically creating test cases, test
    executions and update of the test case status in test execution.""",
    url='nothing'
    auth='Steph Wollgarten'
    author_email='s.wollgarten@gmail.com'
    packages=['pytest_xray']
    install_required=REQUIRED_PACKAGES,
    entry_points={
        'pytest11': ['xray = pytest_xray.plugin', ],
    },
)