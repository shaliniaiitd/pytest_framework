import requests
import json
import pytest
from tests.test_base import BaseTest


class Test_reqres(BaseTest):
    url = 'https://reqres.in/api/'
    headers = {"content-type": "application/json","Accept":"application/json"}

    def test_list_users(self):
        url = self.url + "users"
        self.logger.info("USING QUERY PARAMS")
        self.logger.info(f"Logging into {url}")

        param = {"page": 2}
        resp = requests.get(url,params=param)
        print(url)
        assert resp.status_code == 200

        resp = resp.json()
        assert resp["page"] == 2
        assert len(resp["data"]) == 6

#2
    def test_single_user_not_found(self):
        url1 = self.url + '/23'
        resp = requests.get(url1)

        assert resp.status_code == 404
#3
    def test_get_user_by_id(self,request):
        #self.headers.update({"Accept":"application/json"})

        url1 = self.url  + 'users/4'
        resp = requests.get(url1)

        assert resp.status_code == 200
        assert len(resp.json()) == 2
        assert resp.json()["data"]["id"] == 4

    def test_login_get_jwt(self, request):
        url1 = self.url + "login"

        login_cred = self.env_dict.get("LOGIN_CRED")
        self.logger.info(f"Logging into {url1} with credentials {login_cred}")

        resp = requests.post(url1, data=login_cred,headers=self.headers)
        # data argument corresponds to Body of request.
        # params argument sends the arguments in the URL as query parameter.

        print(resp.text)
        token = resp.json()["token"]
        self.logger.info(f"Got token as {token}")

        assert resp.status_code == 200
    def test_patch_user_created(self,                                                                                                request):
        url1 = self.url + "users/2"
        print(url1)
        data = {
            "name": "morpheus",
            "job": "zion resident"
        }
        self.headers.update({"Authorization": "Bearer QpwL5tke4Pnpja7X4"})
        payload = json.dumps(data)
        flag = 1
        resp = requests.patch(url1,params=data)

        #print(resp.json())

        assert resp.status_code == 200

        # if resp.json()["name"]!= "morpheus"  or resp.json()["job"]!= "zion resident":
        #     pytest.fail("Actual Patch did not happen")
        #     flag = 0
        # assert resp.json()["name"]!= "morpheus"
        # assert resp.json()["job"]!= "zion resident"
        # assert flag==1

    def test_delete(self):
        resp = requests.delete(self.url + '4')

        assert resp.status_code == 204


    def test_create_user_by_data(self):
        self.url +=  'users'
        dict1 = {"name": 'morpheus1',"job": 'leader'}
        print(self.url)
        self.headers.update({"Authorization":"Bearer QpwL5tke4Pnpja7X4"})
        print (self.headers)

        resp = requests.post(self.url,params=dict1, headers=self.headers)
        assert resp.status_code == 201

    def test_create_user_by_json(self):
        dict1 = {"name": 'morpheus1',"job": 'leader'}
        dict1 = json.dumps(dict1)
        dict2 = json.loads(dict1)
        self.url += 'users'

        self.logger.info(self.url)
        self.logger.info(self.headers)
        #self.headers.update({"Authorization": "Bearer QpwL5tke4Pnpja7X4"})
        print(self.headers)
        # we need not specify content-type in headers,
        # requests itself updates it to application/json

        resp = requests.post(self.url,params=dict2, headers=self.headers)
        # Gives 400 error - for POST Method use params argument, not data
        #even params =dict1 works

        assert resp.status_code == 201

    def test_create_user_by_json_file(self):
        self.url += "users"
        #dict1 = {"name": 'morpheus1', "job": 'leader'}

       # resp = requests.post(self.url,data=self.test_data_file_name)
        resp = requests.post(self.url, params=self.test_data_file_name) # Both work
       # print(resp.json())

        assert resp.status_code == 201

    def test_register_get_jwt(self,request):
       url = self.url + 'register'
       data = self.env_dict["REGISTER_CRED"]
       self.logger.info(data)
       resp = requests.post(url,data=json.loads(data))
       self.logger.info(resp.url)
       #data argument corresponds to postman Body (x-www-form-urlencoded format)
       #here json and params arguments wont work.
       #logger.INFO(resp.json()) #{'id': 4, 'token': 'QpwL5tke4Pnpja7X4'}

       assert resp.status_code == 200
       assert resp.json()["id"] == 4
       assert resp.json()["token"] == 'QpwL5tke4Pnpja7X4'

    def test_delay(self):
        url = self.url + 'users'
        param = {"delay": 3}

        resp = requests.get(url,params = param)

        assert resp.status_code == 200
        assert resp.json()["page"] == 1
        assert resp.json()["total"] == 12

    def test_get_single_user(self):
        url = self.url + 'users/2'

        resp = requests.get(url)

        assert resp.status_code == 200
        assert resp.json()["data"]["first_name"] == "Janet"

    def test_list_resource(self):
        url = self.url + "unknown"

        resp = requests.get(url)

        assert resp.status_code == 200
        assert resp.json()["page"] == 1
        assert resp.json()["total"] == 12

    def test_single_resource(self):
        url = self.url + 'unknown/2'

        resp = requests.get(url)
        self.logger.info(url)

        assert resp.status_code == 200
        self.logger.info(resp.json())
        assert resp.json()["data"]["name"] =="fuchsia rose"

    def test_register_unsuccessful(self):
        url = self.url + 'register'
        data = {"email": "sydney@fife"}

        resp = requests.post(url,data=data)

        assert resp.status_code == 400
        assert resp.json() == {"error": "Missing password"}








