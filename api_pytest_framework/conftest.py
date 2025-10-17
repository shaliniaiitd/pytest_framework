
import logging
from logging.handlers import RotatingFileHandler

from configparser import RawConfigParser
import json
from dotenv import dotenv_values
import os
import pytest

REPORT_PATH = "reports"

#Hook-wrapper for Displaying images in pytest-html reports
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        feature_request = item.funcargs['request']

        image_content = feature_request.config.cache.get("image_content", None)
        file_name = feature_request.config.cache.get("image_file", None)
        img_path = os.path.join(REPORT_PATH, "images", file_name)
        extra.append(pytest_html.extras.image(image_content, ''))

    report.extra = extra

@pytest.fixture(scope='class')
def read_test_data(request,test_data_file_name):
    test_data = []
    if os.path.exists(test_data_file_name):
        with open(test_data_file_name, 'r') as data_file:
            json_test_data = json.dumps(data_file)
    request.cls.json_test_data = json_test_data

class Logger:
    def __init__(self, log_file_path, log_level=logging.INFO):
        self.logger = logging.getLogger("test_logger")
        self.logger.setLevel(log_level)

        log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.logger.addHandler(console_handler)

        if log_file_path:
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            log_file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024, backupCount=3)
            log_file_handler.setFormatter(log_formatter)
            self.logger.addHandler(log_file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

@pytest.fixture(scope='session')
def read_config(request):
    pytest_config = RawConfigParser()
    pytest_config.read('pytest.ini')
    request.config.cache.set("pytest_ini", pytest_config)


@pytest.fixture(scope='session')
def read_dot_env(request):
    #load_dotenv(find_dotenv())
    # Load environment variables from the .env file into a dictionary
    env_dict = dotenv_values(".env")
    request.cls.env_dict = env_dict

@pytest.fixture(scope='class')
def create_logger(request):
    if  request.config.getoption("--log-file"):
         log_filename = request.config.getoption("--log-file")
    else:
         log_filename = 'default.log'

    logger = Logger(log_filename, log_level = logging.INFO)
    request.cls.logger =  logger
    return logger

def pytest_addoption(parser):
    parser.addoption("--test-data-file", action="store", default=None, help="Specify the test data filename.")

@pytest.fixture(scope='class')
def test_data_file_name(request):
    request.cls.test_data_file_name = request.config.getoption("--test-data-file")

##SKY
    import os
import subprocess

import pytest
from dotenv import load_dotenv, dotenv_values
from clickhouse_driver import Client as ClickHouseClient
from clickhouse_driver.errors import NetworkError
import time
import re
import paramiko

# Get env data from .env
@pytest.fixture(scope="session")
def get_env_data():
    env_file = ".env"
    load_dotenv(dotenv_path= env_file, override=True)

    return dotenv_values(env_file)



# Port-forwarding
@pytest.fixture(scope="session")
def clickhouse_port_forward(get_env_data):
    """Set up port-forwarding to Clickhouse pod in Kubernetes"""
    try:
        # Get Clickhouse pod name
        cmd = f"kubectl get pods -n {get_env_data['NAMESPACE']} --selector={get_env_data['CLICKHOUSE_SELECTOR']} -o=jsonpath='{{.items[0].metadata.name}}'"
        pod_name = subprocess.check_output(cmd, shell=True).decode().strip()

        # Start port-forward
        port_forward = subprocess.Popen(
            ["kubectl", "port-forward", "-n", get_env_data['NAMESPACE'], pod_name, f"{get_env_data['CLICKHOUSE_PORT']}:9000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for connection
        time.sleep(15)
        yield

        # Cleanup
        port_forward.terminate()

    except Exception as e:
        pytest.skip(f"Could not establish port-forward: {str(e)}")


# Clickhouse Client
@pytest.fixture(scope="session")
def clickhouse_client(clickhouse_port_forward, get_env_data):
    """Create ClickHouse Client Connection"""
    client = ClickHouseClient(
        host=get_env_data['CLICKHOUSE_HOST'],
        port=get_env_data['CLICKHOUSE_PORT'],
        user=get_env_data['CLICKHOUSE_USER'],
        password=get_env_data['CLICKHOUSE_PASSWORD'],
        settings={'use_numpy': False}
    )

    try:
        client.execute("SELECT 1")  # Test Connection
    except NetworkError as e:
        pytest.skip(f"Count not connect to Clickhouse: {str(e)}")

    return client


# Connect to SSH Client
@pytest.fixture(scope="session")
def get_ssh_client(get_env_data):
    ssh_host = get_env_data["SSH_HOST"]
    ssh_port = get_env_data["SSH_PORT"]
    ssh_user = get_env_data["SSH_USER"]
    ssh_password = get_env_data["SSH_PASSWORD"]
    pem_file = get_env_data["PEM_FILE"]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if (pem_file):
        # Load the PEM key
        key = paramiko.RSAKey.from_private_key_file(pem_file)
        ssh.connect(hostname=ssh_host, username=ssh_user, pkey=key)
        print(f"ssh successfully to {ssh_host} using aws.pem!")

    else:
        ssh.connect(hostname=ssh_host, username=ssh_user, password=ssh_password)
        print("ssh successfully to {ssh_host} using password!")

    yield ssh

    # Cleanup
    ssh.close()






#
#
# @pytest.fixture(scope="session", autouse=True)
# def set_env(read_config, read_dot_env, create_logger, get_test_data):
#     # Recreate the Logger object using the stored information
#
#     # request.config.cache.set("logger", logger)
#
#     # Additional setup logic if needed
#     yield
#
# import inspect
#
# import pytest
# @pytest.fixture(scope='class', autouse=True)
# def read_c(request):
#         print(inspect.stack()[1][3])
#         return inspect.stack()[1][3]
