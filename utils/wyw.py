
import asyncio
import json
import time

import httpx
from conf import config
from utils.algo import get_h5st
from utils.coroutines import async_print
from utils.devices import get_random_uuid, get_device
from utils.com import random_number_string


MAX_RETRIES = config.get('JD_WYW_MAX_RETRIES', 5)
RETRY_DELAY = config.get('JD_WYW_RETRY_DELAY', 2)
H5ST_VERSION = '4.8.2'
H5ST_TEMPLATE ='20241015110207316;b11bbcdx2krosso2;afec7;tk03wab071cc418nUZ6AFI2aAdonBfPTJG5ERwj1uLSFtKvZpoUf1ztAuxxjfOw3jEJ4QdYyAEAgttu1gv-JggSRef7d;25a00edcdc80a504edcc12d1d7c387c2;4.8;1728961327316;TKmWZt2Okag6jZw6rNT4yJw_0RDK0NUOcOU6wNUO2uWLeW0I0eg_zNUO2uWL0CA9mCz9jOwJd_QJm_w_lCA_fyTJdWDIf6D_gKT9l6TI0W0I0WvFq5w_x5vO2W0UqOU9y5j_eWj_15jKlCj_kCD9gWDJmyDKzJQIiyzJdyjJfOUOcOk619v71JwO2W0UqO0Ko2zLi_f-xlA8wZBJuNUOcO050WUOMm0OtBfDCBiBGNy5p9vO2uzOpZQ9oRw60WUOMm0Oi_T8zN-_1VU4hdA8KNUOcO09mNUO2uWLZVUOMWTOcOUIhNwO2WUO2uWL0OUOcOkJhNwO2WUO2uWLjSTOcO0JhNwO2WUO2uWLmW0I0CD50NUO2WUOMmUK2uzOiCv_0WUO2W0UqKzJ2uzOjCv_0WUO2W0UqSDL2uzOkCv_0WUO2W0UqOEJoSzLmaB9ixQ70W0I0SD50NUO2WUOMmUK2uzOr5vO2WUO2uWLmW0I0KP70WUO2W0UqWTOcOU70WUO2W0UqWTOcOU9fNUO2WUOMqPOcOU9oBQ5eBwO2W0UqiPO2u2OmthFDtSAiVP7xlg_3Fw80W0I0ST60WUO2W0UbV0I0WP60WUOMm0Og5PObSTKmekKlSDKlOzLlShEDZU9qxA5UVkKmyDKS1SObODK2GA8nNP9oRSOb2-5oxQD0W0I0SA5jNUO2um4;37aa66e350b3049e42193561a5316749'
UA = 'jdapp;android;13.6.0;;;;;;;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 12; HD1903 Build/SKQ1.211113.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046291 Mobile Safari/537.36'


class JdWyw:
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
        eu = random_number_string(16, '5')
        fv = random_number_string(16, '3')

        params = {
            'functionId': function_id,
            'appid': 'signed_wh5',
            'body': json.dumps(body),
            'openudid': eu + fv,
            'eu': eu,
            'fv': fv,
            'screen': '384*854',
            'build': '100090',
            'osVersion': '12',
            'networkType': 'wifi',
            'd_brand': 'OnePlus',
            'd_model': 'HD1903',
            'client': 'android',
            'clientVersion': '13.6.0',
            'partner': 'jingdong',
            't': int(time.time() * 1000),
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
