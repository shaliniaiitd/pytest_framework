import requests
import json
import pytest

@pytest.mark.parametrize("user, passwd", [("admin", "admin"),("admin", "admn")])
def test_autenticate_user(user,passwd):
    resp = requests.get("https://the-internet.herokuapp.com/basic_auth", auth = (user, passwd) )
    assert resp.status_code == 200

# print(resp) #200
#
# resp = requests.get("https://the-internet.herokuapp.com/basic_auth", auth = ("admin", "admn") )
# print(resp) #401 - user unauthorised

#Test user creation


