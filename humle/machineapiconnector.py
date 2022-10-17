import requests
import json
from datetime import datetime, timedelta


class MachineAPIWrapper:
    def __init__(self, host: str, username: str, password: str):
        self._host = host
        self._creds = MachineAPICredentials(host=host, username=username, password=password)
        print("MachineAPIWrapper initialised")

    # def postproducts(self, productspayload: list):
    #     self.executepost(endpoint="/products/Twilfit/2", jsondata={"products": productspayload})

    def postproductsandcategories(self, storename: str, storeid: int, productsandcategories: dict):
        self.executepost(endpoint="/bespokesolutions/{storename}/{storeid}".format(storename=storename,
                                                                                   storeid=storeid),
                         jsondata=productsandcategories)

    def executepost(self, endpoint: str, body: dict = None, jsondata=None):
        response = requests.post(self._host + endpoint, data=body, json=jsondata, headers=self.requestheader())

        if not response.ok:
            print(response.status_code)
            print(response.text)
            raise requests.HTTPError

        return response

    def requestheader(self) -> dict:
        return {"Authorization": "Bearer {}".format(self._creds.accesstoken)}


class MachineAPICredentials:
    def __init__(self, host: str, username: str, password: str):
        self._host = host
        self.username = username
        self.password = password
        self._accesstoken, self._refreshtoken, self._expirationtime = self.login()

    @property
    def accesstoken(self) -> str:
        if not self.valid():
            # Refresh access token
            self.refreshaccesstoken()
        return self._accesstoken

    def login(self) -> (str, str, datetime):
        url = self._host + "/login"
        body = {
            "username": self.username,
            "password": self.password
        }
        response = requests.post(url=url, data=body)

        if not response.ok:
            print(response.status_code)
            print(response.text)
            raise requests.HTTPError

        try:
            jsonresponse = json.loads(response.text)
            expiration = datetime.now() + timedelta(minutes=14)
            return jsonresponse['accesstoken'], 'deprecated', expiration
        except (json.JSONDecodeError, TypeError):
            raise PermissionError

    def valid(self) -> bool:
        delta = datetime.now() - self._expirationtime
        if delta.total_seconds() > 0:
            return False
        return True

    def refreshaccesstoken(self):
        self._accesstoken, self._refreshtoken, self._expirationtime = self.login()
        return
