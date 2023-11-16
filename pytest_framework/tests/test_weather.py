import requests
import json
import pytest
from tests.test_base import BaseTest
from PIL import Image
from io import BytesIO
import os
import base64
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# driver = webdriver.Edge()
#
# url = 'https://home.openweathermap.org/users/sign_up'
#
# driver.get(url)
#
# input_username = driver.find_element(By.ID, "user_username" )
# input_username.send_keys("shalini")
#
# input_email = driver.find_element(By.ID, "user_email" )
# input_email.send_keys("shalinia.iitd@gmail.com")
#
# input_password = driver.find_element(By.ID, "user_password")
# input_password.send_keys("api_password")
#
# input_confirm_password = driver.find_element(By.ID,"user_password_confirmation")
# input_confirm_password.send_keys("api_password")
#
# chkbox1 = driver.find_element(By.XPATH, "//*[contains(text(),'16 years')] /input[@type = 'checkbox']")
# chkbox1.click()
#
# chkbox2 = driver.find_element(By.XPATH,"//*[contains(text(),'I agree with')] /input[@type = 'checkbox']")
# chkbox2.click()
# import time
# time.sleep(3)
# chkbox3 = driver.find_element((By.XPATH, "//*[starts-with(text(),'System news')] /input[@type = 'checkbox']"))
# chkbox3.click()
# time.sleep(3)
# chkbox4 = driver.find_element((By.XPATH, "//*[contains(text(),'Product news')] /input[@type = 'checkbox']"))
# chkbox4.click()
#
# time.sleep(3)
# chkbox5 = driver.find_element((By.XPATH, "//*[contains(text(),'Corporate news')] /input[@type = 'checkbox']"))
# chkbox5.click()
#
# time.sleep(5)
# captcha = driver.find_element(By.XPATH, '//span[@id = "recaptcha-anchor"]')
# captcha.click()
# time.sleep(3)
# create_btn = driver.find_element(By.XPATH, '//*[@value="Create Account"]')
# create_btn.click()


class Test_weather(BaseTest):

      headers = {"content-type": "application/json","Accept":"application/json"}

      url = 'https://home.openweathermap.org/'


      @pytest.mark.parametrize("cityname, state_name, country_code", [('New Delhi','Delhi', 'IN')])
      def test_get_new_delhi_coordinates(self,cityname, state_name, country_code, request ):
          url = 'http://api.openweathermap.org/geo/1.0/direct'
          params = {"q":f"{cityname},{state_name},{country_code}", "limit": 5, "appid": self.env_dict["API_KEY"] }


          resp = requests.get(url,params = params)
          self.logger.info(resp.url)
          assert resp.status_code == 200
          self.logger.info(resp.json())
          delhi_lat = resp.json()[0]["lat"]
          assert delhi_lat == 28.6138954
          delhi_lon = resp.json()[0]["lon"]
          assert delhi_lon == 77.2090057

          request.config.cache.set("lat",28.6138954)
          request.config.cache.set("log",77.2090057)

      def test_register_a_station(self,request):
          url = "http://api.openweathermap.org/data/3.0/stations"

          data = {
              "external_id": "SF_TEST001",
              "name": "San Francisco Test Station",
              "latitude": 37.76,
              "longitude": -122.43,
              "altitude": 150
            }
          params =  {"appid": self.env_dict["API_KEY"]}
          request.config.cache.set("params",params)

          resp = requests.post(url,json = data, params = params)

          assert resp.status_code == 201
          st_id = resp.json()["ID"]
          st_name = resp.json()["name"]
          assert st_name == 'San Francisco Test Station'

          self.logger.info(f"st_id =  {st_id}")
          request.config.cache.set("st_id", st_id)

          request.config.cache.set("station_name",st_name)

      def test_send_measurements_for_station(self,request):
          url = 'http://api.openweathermap.org/data/3.0/measurements'

          st_id = request.config.cache.get("st_id",None)
          self.logger.info(f"Got st_id =  {st_id}")

          data = {"station_id": st_id ,
                "dt": 1479817340,
                "temperature": 18.7,
                "wind_speed": 1.2,
                "wind_gust": 3.4,
                "pressure": 1021,
                "humidity": 87,
                "rain_1h": 2,
                "clouds": [
                  {
                 "condition": "NSC"
                 }
                ]
            }

          params = request.config.cache.get("params", None)
          print(params)
          resp = requests.get(url,json = json.dumps(data), params = params, headers = {"content-type": 'application/json'})

          assert resp.status_code == 400
          assert resp.json()["code"] == 400001
          assert resp.json()["message"] == "bad station id"
          #seeming issue with api.Got same resul with Postman and on browser as well.

      # Request Chaining - get info for the station created in this session.

      def test_get_station_info(self,request):
          st_id = request.config.cache.get("st_id", None)
          self.logger.info(f"Got st_id =  {st_id}")

          url = f'http://api.openweathermap.org/data/3.0/stations/{st_id}'
          params = {"appid":self.env_dict["API_KEY"]}
          resp = requests.get(url,params=params)
          print(resp.url)
          assert resp.status_code == 200
          assert resp.json()["id"] == st_id
          assert resp.json()["external_id"]== "SF_TEST001"

#Negative test cases
      def test_get_station_info__negative_invalid_st_id(self,request):
          st_id = request.config.cache.get("st_id", None)
          self.logger.info(f"Got st_id =  {st_id}a")

          url = f'http://api.openweathermap.org/data/3.0/stations/{st_id}a'
          params = {"appid": self.env_dict["API_KEY"]}
          resp = requests.get(url, params=params)
          print(resp.url)
          assert resp.status_code == 400
          assert resp.json()["code"] == 400002
          assert resp.json()["message"] == "Station id not valid"

      def test_get_station_info_negative_wo_apikey(self,request):
          st_id = request.config.cache.get("st_id", None)
          self.logger.info(f"Got st_id =  {st_id}")

          url = f'http://api.openweathermap.org/data/3.0/stations/{st_id}'
          params = {"appid": self.env_dict["API_KEY"]}
          resp = requests.get(url)
          print(resp.url)
          assert resp.status_code == 401

          assert resp.json()["cod"] == 401
          assert resp.json()["message"] == "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."

      def test_put_station_info(self, request):
          data = {"name":"Changed Station name",
                     "external_id": "1"
                    }
          st_id = request.config.cache.get("st_id", None)
          self.logger.info(f"Got st_id =  {st_id}")

          url = f'http://api.openweathermap.org/data/3.0/stations/{st_id}'
          params = {"appid": self.env_dict["API_KEY"]}
          resp = requests.put(url,params =params, json=data, headers={"Accept": "application/text"})
          print(resp.url)
          expected_resp = "{'id': '6553fbae8885c200018ae762', 'created_at': '2023-11-14T22:58:54.585Z', 'updated_at': '2023-11-15T08:50:09.932249796Z', 'external_id': '1', 'name': 'Changed Station name', 'longitude': 0, 'latitude': 0, 'altitude': None, 'rank': 0}"
          exp_resp =  {"id":"6553fbae8885c200018ae762","created_at":"2023-11-14T22:58:54.585Z","updated_at":"2023-11-15T09:04:04.903698465Z","external_id":"1","name":"Changed Station name","longitude":0,"latitude":0,"altitude":None,"rank":0}

          self.logger.info(f"resp.text  {resp.text}")

          assert expected_resp == str(resp.json())



          assert resp.status_code == 200


      def test_widget_daily_8days_forecast(self):
        url = "https://openweathermap.org/widgets-constructor"

        resp = requests.get(url)

        assert resp.status_code == 200
        for key, value in resp.headers.items():
            print(key,value)
        assert resp.headers["Content-Type"] == 'text/html; charset=UTF-8'
        assert resp.headers["Content-Encoding"] == 'gzip'

      def test_5day_3hour_forecast(self,request):
          url = "https://api.openweathermap.org/data/2.5/forecast"

          lat = request.config.cache.get("lat", None)
          lon = request.config.cache.get("log", None)
          appid = self.env_dict["API_KEY"]
          print(lon)
          params = {"lat":lat, "lon":lon, "appid":appid}
          print(params)
          resp = requests.get(url,params=params)

          self.logger.info(resp.url)


          assert resp.status_code == 200
          assert resp.json()["city"]["coord"]["lat"] == round(lat,4)
          assert resp.json()["city"]["coord"]["lon"] == round(lon,4)
          assert resp.json()["city"]["country"] == "IN"

      @pytest.mark.parametrize("map, zoom, x, y",[
          ("clouds_new", 1,1,1),
          ("precipitation_new", 1,1,1),
          ("pressure_new", 1,1,1),
          ("wind_new",1,1,1),
          ("temp_new", 1,1,1)])
      def test_weather_maps(self, request, map, zoom, x,y):

          appid = self.env_dict["API_KEY"]
          url = f"https://tile.openweathermap.org/map/{map}/{zoom}/{x}/{y}.png"

          params = {"appid": appid}

          resp = requests.get(url, params = params)
          print(resp.url)
          if resp.status_code == 200 and resp.headers["Content-Type"] == "image/png":
                  # Open the image using PIL
                  img = Image.open(BytesIO(resp.content))

                  # Display the image (opens the default image viewer)
                  #img.show()

                  # Save the image to a file (optional)
                  image_file = fr"reports\images\{map}.png"
                  # Ensure the directory exists, create it if not
                  os.makedirs(os.path.dirname(image_file), exist_ok=True)
                  img.save(image_file)

                  # Convert the image to base64
                  with open(image_file, "rb") as image_file:
                      image_content = base64.b64encode(image_file.read()).decode('utf-8')

                  request.config.cache.set("image_name", map)
                  request.config.cache.set("image_file",image_file.name )
                  request.config.cache.set("image_content", image_content)

          else:
              print(f"Failed to retrieve the image. Status code: {resp.status_code}")




#
#     def test_register_get_api(self,request):
#         resp = requests.get('https://home.openweathermap.org/users/sign_up')
#         assert resp.status_code == 200