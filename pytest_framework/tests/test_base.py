import pytest
@pytest.mark.usefixtures("create_logger","read_dot_env","test_data_file_name")
class BaseTest():
    pass


    # @classmethod
    # def setup(self,request,read_dot_env):
    #     self.config =  request.config.cache.get("pytest_ini")

    # def (self,create_logger,read_config,read_dot_env):
    #     self.logger = create_logger
    #     self.config = read_config
    #     self.env = read_dot_env
