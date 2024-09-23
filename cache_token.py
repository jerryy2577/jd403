import asyncio
import json
import os
import time
import httpx
from utils.algo import get_sign
from utils.com import match_value_from_cookie, unquote_pt_pin
from utils.proxy import get_proxies
from utils.coroutines import async_print, start


async def get_isv_token(cookie, **kwargs):
    """
    :return:
    """
    try:
        headers = {
            'user-agent': 'okhttp/3.12.16;jdmall;android;version/13.1.0;build/99208;',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
        }
        resp = get_sign('isvObfuscator', json.dumps({"id": "", "url": "https://lzkj-isv.isvjcloud.com"}))
        url = 'https://api.m.jd.com/client.action?functionId=isvObfuscator&' + resp['body']
        response = httpx.post(url, headers=headers, proxies=get_proxies())
        return response.json().get('token', None)
    except Exception as e:
        await async_print("获取Token失败, {}".format(e.args))


async def write_token(path, pin, token):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    try:
        with open(path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
    except Exception as e:
        await async_print(f"打开文件:{path}失败, {e.args}")
        data = dict()

    data[pin] = {
        'expires': int(time.time() * 1000) + 60 * 29 * 1000,
        'val': token,
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


async def save_faker3_token(pin, token):
    """
    :param pin:
    :param token:
    :return:
    """
    path = '/ql/data/scripts/shufflewzc_faker3_main/utils/token.json'
    await write_token(path, pin, token)


async def save_jdmax_token(pin, token):
    """
    :param pin:
    :param token:
    :return:
    """
    path = '/ql/data/scripts/9Rebels_jdmax/utils/token.json'
    await write_token(path, pin, token)


async def save_jdm_token(pin, token):
    """
    :param pin:
    :param token:
    :return:
    """
    path = '/ql/data/scripts/6dylan6_jdm/utils/token.json'
    await write_token(path, pin, token)


async def cache_token(jd_ck, **kwargs):
    pin = unquote_pt_pin(match_value_from_cookie(jd_ck))
    await async_print("正在获取Token!")
    token = await get_isv_token(jd_ck, **kwargs)
    if token:
        await save_faker3_token(pin, token)
        await save_jdmax_token(pin, token)
        await save_jdm_token(pin, token)
        await async_print("成功获取Token!")

    await asyncio.sleep(1)

if __name__ == '__main__':
    start(cache_token, '缓存Token', max_concurrent=3)
