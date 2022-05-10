from enum import Enum
import datetime
import base64
import json
from typing import Tuple


import urllib3
from Crypto.Hash import CMAC
from Crypto.Cipher import AES


_pysesame_debug = False
def set_debug_mode(flag):
    global _pysesame_debug
    _pysesame_debug = flag

class SESAME_CMD(Enum):
    LOCK = 82
    UNLOCK = 83
    TOGGLE = 88


class Sesame:
    """Control Sesame4.

    This class can unlock, lock and toggle doorkey with Sesame4.

    Sesame4 is door lock IoT device. It's product of CANDY HOUSE, Inc.
    productpage-japanese(https://jp.candyhouse.co/products/sesame4).

    This class control Sesame4 as WebAPI.
    document-japanese(https://doc.candyhouse.co/ja/SesameAPI).
    """

    def __init__(self, *, uuid: str = None, api_key: str = None, secret_key: str = None, file_path=None) -> None:
        """Sesame class constructor.

        Setup valiables required to connect Sesame4.
        There are two kind of setup.
        1. Directly setup specific keys(uuid, api_key, secret_key).
            Sesame(uuid = MY_UUID, api_key = MY_API_KEY, secreat_key = MY_SECRET_KEY)
        2. Set config file path. That is json format.
            Sesame(file_path = "my_sesame_keys.json")
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

    def get_status(self) -> Tuple[bool, bytes]:
        """
        Returns:
            First is True if succeded to get status. False if failed.
            Second is data bytes.
        """
        r:urllib3.HTTPResponse  = self._http.request(
            'GET',
            url=f'https://app.candyhouse.co/api/sesame2/{self._uuid}',
            headers={'x-api-key': self._api_key})

        if _pysesame_debug:
            print(r.status)
            print(r.data)

        return r.status == 200, r.data

    def get_log(self, page: int = 1, lg: int = 50) -> Tuple[bool, bytes]:
        """
        Returns:
            First is True if succeded to get status. False if failed.
            Second is data bytes.
        """
        r:urllib3.HTTPResponse = self._http.request(
            'GET',
            url=f'https://app.candyhouse.co/api/sesame2/{self._uuid}/history?page={page}&lg={lg}',
            headers={'x-api-key': self._api_key})

        if _pysesame_debug:
            print(r.status)
            print('\n'.join(map(str, (json.loads(r.data)))))

        return r.status == 200, r.data

    def post_cmd(self, cmd) -> bool:
        url = f'https://app.candyhouse.co/api/sesame2/{self._uuid}/cmd'

        headers = {'x-api-key': self._api_key}

        history = 'pysesame'
        byte_history = bytes(history, 'utf-8')
        base64_history = base64.b64encode(byte_history).decode()

        timestamp = int(datetime.datetime.now().timestamp())
        mes = timestamp.to_bytes(4, byteorder='little')
        mes = mes.hex()[2:8]
        cmac = CMAC.new(bytes.fromhex(self._secret_key), ciphermod=AES)
        cmac.update(bytes.fromhex(mes))
        sign = cmac.hexdigest()

        body = {
            'cmd': cmd,
            'history': base64_history,
            'sign': sign
        }
        r:urllib3.HTTPResponse  = self._http.request(
            'POST',
            url=url,
            headers=headers,
            body=json.dumps(body))

        if _pysesame_debug:
            print(r.status)
    
        return r.status == 200

    def lock(self) -> bool:
        """
        Returns:
            True if succeded to get status. False if failed.
        """
        return self.post_cmd(SESAME_CMD.LOCK.value)

    def unlock(self) -> bool:
        """
        Returns:
            True if succeded to get status. False if failed.
        """
        return self.post_cmd(SESAME_CMD.UNLOCK.value)

    def toggle(self) -> bool:
        """
        Returns:
            True if succeded to get status. False if failed.
        """
        return self.post_cmd(SESAME_CMD.TOGGLE.value)
