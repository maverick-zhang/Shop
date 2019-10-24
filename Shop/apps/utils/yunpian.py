import json

import requests


class YunPian:
    """
    短信验证码
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobil):
        """
        发送短信
        :param code:验证码
        :param mobil: 手机号
        :return: TRUE OR FALSE 发送是否成功
        """
        params = {
            "api_key": self.api_key,
            "mobil": mobil,
            "text": "这是一个测试用的短息{code}".format(code=code)
        }
        response = requests.post(self.single_send_url, data=params)
        to_dict = json.loads(response)
        return to_dict
