import os
import pytest
import requests
from tests.test_base import BaseTest
import json

class Test_auth(BaseTest):
#app = App(read_config,get_test_data,get_logger)

   # def test_basic_auth(self):
   #
   #    headers = {"Accept": "application/json"}
   #
   #    resp = requests.post(data={"email": "eve.holt@reqres.in","password": "pistol"}, url="https://reqres.in/api/register" )
   #
   #
   #    assert resp.status_code == 200
   #
   #    assert resp.headers["Content-Type"] == "text/html;charset=utf-8"

   @pytest.mark.parametrize("user, passwd, expected", [("admin", "admin",200),("admin", "admn",401)])
   def test_autenticate_user(self,user,passwd,expected):
       resp = requests.get("https://the-internet.herokuapp.com/basic_auth", auth = (user, passwd) )
       assert resp.status_code == expected

   # def test_digest_authentication(self):
   #
   #    headers = {"Accept": "application/json"}
   #
   #    #resp = requests.get(url="https://the-internet.herokuapp.com/digest_auth",auth=("admin", "admin") )
   #
   #    resp = requests.post("https://reqres.in/api/login",data={"email": "eve.holt@reqres.in",
   #     "password": "cityslicka"})
   #
   #    self.logger.info(f"RESPONSE FOR DIGEST_AUTHENTICATION {resp.content}")
   #
   #    assert resp.status_code == 200
   #
   #    #assert resp.headers["Content-Type"] == "text/html;charset=utf-8"

   # def test_login_get_jwt(self,request):
   #    login_cred = json.loads(os.getenv("LOGIN_CRED"))
   #    print(login_cred)
   #    resp = requests.post("https://reqres.in/api/login", data=login_cred)
   #    self.logger.info(resp.json()) #{'token': 'QpwL5tke4Pnpja7X4'}
   #
   #    #request.config.cache.set("login_cred",{"email": "eve.holt@reqres.in","password": "cityslicka","token": resp.json()["token"]})
   #
   #    assert resp.status_code == 200

   # def test_register_get_jwt(self,request):
   #    data = json.loads(os.getenv("REGISTER_CRED"))
   #    resp = requests.post("https://reqres.in/api/register",data=data )
   #    print(data)
   #    self.logger.info(resp.json()) #{'id': 4, 'token': 'QpwL5tke4Pnpja7X4'}
   #
   #    assert resp.status_code == 200


