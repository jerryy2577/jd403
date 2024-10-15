import httpx
import sys
from conf import config
from utils.proxy import get_no_proxies


def get_sign(fn: str, body: str):
    """
    :return:
    """
    try:
        url = config.JY_SIGN_URL
        if not url:
            url = 'https://www.crdsdbyyd.xyz/sign'

        data = {
            "fn": fn,
            "body": body,
        }
        r = httpx.post(url, json=data, proxies=get_no_proxies())
        return r.json()
    except Exception as _:
        print('获取sign失败, 请检查配置!')
        return {}


def get_h5st(pin, body, ua, h5st='', version='4.7.4'):
    try:
        url = config.JY_H5ST_URL
        if not url:
            url = 'https://www.crdsdbyyd.xyz/h5st'

        # 准备请求数据
        data = {
            "version": version,
            "ua": ua,
            "body": body,
            "h5st": h5st,
            "pin": pin,
            "debug": False
        }
        r = httpx.post(url, json=data, proxies=get_no_proxies())
        data = r.json()
        if data.get('code') != 200:
            return ''
        return r.json().get('body', {}).get('h5st', '')
    except Exception as _:
        return ''


if __name__ == '__main__':
    print(get_sign(fn='isvObfuscator', body="{\"url\":\"https://lzkj-isv.isvjd.com\",\"id\":\"\"}"))
