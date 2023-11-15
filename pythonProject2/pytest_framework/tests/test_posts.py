import time
import os


import requests

import pytest

from utilities.custom_logger import Logger


LOGGER = Logger("../logs/posts_test.log")
URL = "https://jsonplaceholder.typicode.com/posts"
def calculate_time(func):
    def inner(*args):
        start = time.time()
        func(*args)
        end = time.time()
        duration = end-start
        LOGGER.info(f" Function {func.__name__} took {duration:.8f} seconds")
    return inner


@calculate_time
def test_create_user_by_payload():
    payload = {
        "userId": 12,
        "title": "user12",
        "body": "body for user 12"
    }

    resp = requests.post(URL, data=payload)
    print(resp.json())  # {'userId': '12', 'title': 'user12', 'body': 'body for user 12', 'id': 101}

    #id = resp.json()['id']
    assert resp.status_code == 201

    return resp

@calculate_time
def test_get_all_posts():
    URL1 = URL
    LOGGER.info("STARTING test_get_all_posts")
    resp = requests.get(URL1,headers={"accept":"application/json"})
    print(URL1)
    json_resp = resp.json()

    LOGGER.info(len(json_resp))

    assert resp.status_code == 200
    assert len(json_resp) == 100

@calculate_time
@pytest.mark.parametrize("userId, id , exp_st_code", [(1,3, 200), (6,55,200)])
def test_get_post_by_userId_id(*args):
    for arg in args:
        params = {"userId":arg[0], "id": arg[1]}
        resp = requests.get(URL,params )

        assert resp.status_code == arg[2]
def test_creation(request):
    request.config.cache.set('shared', 'spam')
    assert True

def test_deletion(request):
    assert request.config.cache.get('shared', None) == 'spam'

def test5():
    assert True
    return(5)

def test6():
    id = test5()
    assert id == 5

def test1(request):
    request.config.cache.set("var",'value_set')
    assert True

def test2(request):
    assert request.config.cache.get("var",None) == 'value_set'


# @pytest.fixture
# def set_env():
# LOGGER = Logger("../logs/posts_test.log")
# #LOGGER = Logger()
# #URL = get_url('base_url') + 'posts'
# URL = "www.yahoo.com"
#print(URL)
# def get_url():
#     base = "https://jsonplaceholder.typicode.com/"
#     endpoint = 'posts'
#     url = base + endpoint
#     return url



















# def test_user_creation_json():
#     #read payload from a file
#     logger = LogGen.loggen()
#     logger.info("START test user creation")
#
#     base = rc.get_url('base_url')
#
#     endpoint = 'post'
#     url = base + endpoint
#     json_data = self.json_test_data
#     # print("JSON_DATA:", json_data)
#
#     payload = json.loads(json_data)  #converts json to python
#     print("PAYLOAD:",payload)
#
#     headers = {"Content-Type": "application/json"}
#     resp = requests.post(url, data = json_data, headers=headers)
#     print(resp.status_code)
#     print(resp.json())
    # resp = requests.post(url,json=payload)  #Python payload that needs to be serialized- converted to JSON format.
    # print(resp.status_code)
    # print(resp.json())
#print(resp.headers['Content-Length'])

#user with auth, get the token returned from server in response

# payload = {
#     "email": "eve.holt@reqres.in",
#     "password": "pistol"
# }
# url = base + "/api/register"
# resp = requests.post(url, data = payload)
# print(resp)
# print(resp.json()['token'])
# print(resp.headers)
#