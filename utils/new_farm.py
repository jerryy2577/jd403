
import asyncio
import json
import httpx
from conf import config
from utils.algo import get_h5st
from utils.coroutines import async_print
from utils.devices import get_random_uuid, get_device


MAX_RETRIES = config.get('JD_FARM_WATER_MAX_RETRIES', 5)
RETRY_DELAY = config.get('JD_FARM_WATER_RETRY_DELAY', 2)
H5ST_VERSION = '4.2.0'
H5ST_TEMPLATE ='20241011152332638;twwpam93zwpttzj6;c57f6;tk03w9fab1bfd18n4RruwgKCP1Ws5tEf29RpdTR2Wq1lngVRbtNOxDW87Pi-QGIfHXLHOTQdkvmEB7vOUMrCnEzhV5eN;a1a9d2443f1192a98bcf64444f847a2d0ad7cae09fbc8fe4940410869760290f;4.2;1728631412638;e9f6ec1bab0ebf8ad0759c5c9ae319e1030045229d00313e52233354c9b748d440890c4e82bfeb1b5affb9c351b4b40255de0468a9ba0782ea6005d65e47c3ce1a9b08cf55d1d79918f718a4d22b7c657560901895d4b32bfcb185941d63f21779315a9be7a949d4dc391c848e49e4aef8cfa80c941788e87d5c0b051ece05a6af1e9f5dc38d7047cf9caa4fe452a916122197a08b009a693f78df6ad6b9eda5808905df82ca88b3a489b5986fdb9ef36b83200219399783a2976ecf86b363cc2dda0d716e4df2490e3ead7a6d04f2206dd046f0b39da10663f3eab09fc37e448b19664bc8f9251f75bd77aa6b28036966367e88eb12b446cf6a5c8bdc3cd9cee0ff3b9edc9904cc0f1f6ef8448d05252967a9bb0c669306c2e20a56b9892fc9cd4d47a6f2ee138377060a0f3202ad72'
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
    async def create_params(cls, function_id, body, pin, h5st_template=''):
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
            if not h5st_template:
                h5st_template = H5ST_TEMPLATE

            h5st_body = get_h5st(pin, params, UA, h5st_template, H5ST_VERSION)
            params['h5st'] = h5st_body['h5st']
        except Exception as e:
            await async_print(f'获取h5st失败, {e.args}')
            params['h5st'] = H5ST_TEMPLATE
        return params
