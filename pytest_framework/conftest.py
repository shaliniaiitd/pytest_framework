import pytest
import os
import logging
from logging.handlers import RotatingFileHandler

from configparser import RawConfigParser
from dotenv import load_dotenv, find_dotenv
import json
from dotenv import dotenv_values

import os
import base64
from datetime import datetime
from PIL import Image
from io import BytesIO
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

        # Assuming you have the image content in a variable (replace this with the actual variable)
        image_content = feature_request.config.cache.get("image_content", None)
        file_name = feature_request.config.cache.get("image_file", None)
        img_path = os.path.join(REPORT_PATH, "images", file_name)


        extra.append(pytest_html.extras.image(image_content, ''))

    report.extra = extra

@pytest.fixture(scope='class')
def read_test_data(request,test_data_file_name):
    test_data = []
    # if  request.config.getoption("--test_data-file"):
    #      log_filename = request.config.getoption("--log-file")
    # else:
    #      log_filename = 'default.log'
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


@pytest.fixture(scope='class')
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