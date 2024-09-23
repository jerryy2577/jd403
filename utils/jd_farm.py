
import asyncio
import json
import random
import httpx
from conf import config
from utils.algo import get_h5st
from utils.coroutines import start, async_print
from utils.devices import get_random_uuid, get_device
from utils.proxy import get_proxies


MAX_RETRIES = config.get('JD_FARM_WATER_MAX_RETRIES', 5)
RETRY_DELAY = config.get('JD_FARM_WATER_RETRY_DELAY', 2)
H5ST_VERSION = '4.2.0'
H5ST_TEMPLATE ='20240909102640856;ttpigz3ampawwmp7;28981;tk03wa2e71bca18n1r7m5uak3Rfzy7Cs6xXHAw1kyGlZpd0NF1_w6AwDxD3Pm8UFCeHG0b0dFQWosTthe_tRCD-P9vo0;aa1e2c96d477fsf7d3921b9e7830124a74fc3dec04cd2660f87648d6a8a6d4ece;4.2;1725848800856;e9f6ec1bab0ebf8ad0759c5c9ae319e1030045229d00313e52233354c9b748d440890c4e82bfeb1b5affb9c351b4b40255de0468a9ba0782ea6005d65e47c3ce1a9b08cf55d1d79918f718a4d22b7c65e61fc91af52adcc9ddf93b7254ca5058724283d8e0bfcb8e3c27aab701a59902466d78ee12bc5280d8fb0a94414aaf757698c6dae127c38c1ebc40433528dbf33590d4edc09e1ee5f872f4ed4d2c9403323b92664ad68f919fbad57588e160733181083cc7dde39c06289da19c42b7ad4f5d5bb01b92896c35c0f84763b8a83dcb914f3d2c59c22fe1431b2c4702b658f27170a18ce5f112caa4400e8c467cf42fdf44468fb13aba809ee696221a44a0effbe5ad4db07ee188ac11a18391138f0c69e22507d013db67fdb1fc9cad321f11407d72b0ae71534564c07c40b05788'
UA = 'jdapp;android;12.6.6;;;;;;Mozilla/5.0 (Linux; Android 14; HD1905 Build/SKQ1.211113.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.103 Mobile Safari/537.36'


class JdFarm:

    @classmethod
    async def post(cls, url, params, **kwargs):
        attempt = 0
        while attempt < MAX_RETRIES:
            try:
                client = kwargs.get('client')
                response = await client.post(url, data=params, timeout=5)
                if response.status_code == 403:
                    await async_print(f"403 Forbidden: 重试({attempt + 1}/{MAX_RETRIES})...")
                    attempt += 1
                    await asyncio.sleep(RETRY_DELAY)
                    continue
                return response.json()
            except httpx.RequestError as e:
                await async_print(f"请求错误: {e} - 重试({attempt + 1}/{MAX_RETRIES})...")
            except Exception as e:
                await async_print(f"未知异常: {e} - 重试({attempt + 1}/{MAX_RETRIES})...")

            attempt += 1
            await asyncio.sleep(RETRY_DELAY)

        return {'code': 888, 'message': f'超过最大重试次数{MAX_RETRIES}'}

    @classmethod
    async def create_params(cls, function_id, body, pin):
        device_brand, device_model = get_device()
        params = {
            'appid': 'signed_wh5',
            'functionId': function_id,
            'wqDefault': 'false',
            'body': json.dumps(body),
            'clientVersion': '12.6.6',
            'client': 'android',
            'screen': '384*812',
            'build': '99162',
            'osVersion': '14',
            'networkType': 'wifi',
            'd_brand': device_brand,
            'd_model': device_model,
            'uuid': get_random_uuid(),
            'x-api-eid-token': ''
        }
        try:
            h5st_body = get_h5st(pin, params, UA, H5ST_TEMPLATE, H5ST_VERSION)
            params['h5st'] = h5st_body['h5st']
        except Exception as e:
            await async_print(f'获取h5st失败, {e.args}')
            params['h5st'] = H5ST_TEMPLATE
        return params
