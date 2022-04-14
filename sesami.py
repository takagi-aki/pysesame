from enum import Enum
import datetime
import base64
import json


import urllib3
from Crypto.Hash import CMAC
from Crypto.Cipher import AES


class SESAMI_CMD(Enum):
    LOCK = 82
    UNLOCK = 83
    TOGGLE = 88


class Sesami:
    """Operate Sesami4 class.

    This class can unlock, lock and toggle doorkey with Sesami4.

    Sesami is door lock IOT device.
    productpage-japanese(https://jp.candyhouse.co/products/sesame4).

    This class operate Sesami4 as WebAPI.
    document-japanese(https://doc.candyhouse.co/ja/SesameAPI).
    """

    def __init__(self, *, uuid: str = None, api_key: str = None, secret_key: str = None, file_path=None) -> None:
        """Sesami class constructor.

        Setup valiables required to connect Sesami.
        There are two kind of setup.
        1. Directly setup specific keys(uuid, api_key, secret_key).
            Sesami(uuid = MY_UUID, api_key = MY_API_KEY, secreat_key = MY_SECRET_KEY)
        2. Set config file path. That is json format.
            Sesami(file_path = "my_sesami_keys.json")
        """
        self._http = urllib3.PoolManager()
        if(file_path is not None):
            with open(file_path, mode='r') as f:
                data = json.loads(f.read())
                self._uuid = data["UUID"]
                self._api_key = data["API_KEY"]
                self._secret_key = data["SECRET_KEY"]
        elif (uuid is not None) and (api_key is not None) and (secret_key is not None):
            self._uuid = uuid
            self._api_key = api_key
            self._secret_key = secret_key
        else:
            raise ValueError

    def get_status(self):
        r = self._http.request(
            'GET',
            url=f'https://app.candyhouse.co/api/sesame2/{self._uuid}',
            headers={'x-api-key': self._api_key})
        print(r.status)
        print(r.data)

    def get_log(self, page: int = 1, lg: int = 50):
        r = self._http.request(
            'GET',
            url=f'https://app.candyhouse.co/api/sesame2/{self._uuid}/history?page={page}&lg={lg}',
            headers={'x-api-key': self._api_key})
        print(r.status)
        print('\n'.join(map(str, (json.loads(r.data)))))

    def post_cmd(self, cmd):
        url = f'https://app.candyhouse.co/api/sesame2/{self._uuid}/cmd'

        headers = {'x-api-key': self._api_key}

        history = 'pysesami'
        base64_history = base64.b64encode(bytes(history, 'utf-8')).decode()

        ts = int(datetime.datetime.now().timestamp())
        message = ts.to_bytes(4, byteorder='little')
        message = message.hex()[2:8]
        cmac = CMAC.new(bytes.fromhex(self._secret_key), ciphermod=AES)

        cmac.update(bytes.fromhex(message))
        sign = cmac.hexdigest()

        body = {
            'cmd': cmd,
            'history': base64_history,
            'sign': sign
        }
        r = self._http.request(
            'POST',
            url=url,
            headers=headers,
            body=json.dumps(body))

        print(r.status)

    def lock(self):
        self.post_cmd(SESAMI_CMD.LOCK.value)

    def unlock(self):
        self.post_cmd(SESAMI_CMD.UNLOCK.value)

    def toggle(self):
        self.post_cmd(SESAMI_CMD.TOGGLE.value)
