# _*_ coding:utf-8 _*_
import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        # restfull
        # json
        if r.status_code !=200:
            return {} if return_json else ''
        return r.json() if return_json else r.text



