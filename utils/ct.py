import os
import sys
from urllib.parse import unquote

import httpx

from conf import config
from utils.proxy import get_no_proxies


def _get_all_jd_ck_from_env():
    cks = os.environ.get('JD_COOKIE', None)
    if not cks:
        return []
    return cks.split('&')


class CT:
    def __init__(self):
        self._ct_url = config.JY_CT_URL
        self._ct_client_id = config.JY_CT_CLIENT_ID
        self._ct_client_secret = config.JY_CT_CLIENT_SECRET
        self.client = httpx.Client(base_url=f'{config.JY_CT_URL}/open', proxies=get_no_proxies())
        self._auth()

    def _auth(self):
        try:
            params = {
                'client_id': self._ct_client_id,
                'client_secret': self._ct_client_secret,
            }
            r = self.client.get(f'/auth/token', params=params)
            data = r.json()
            if data.get('code') == 200:
                token = ' '.join([data['data']['token_type'], data['data']['token']])
                self.client.headers.update({"authorization": token})
            else:
                print('获取容器Token失败, 请检查配置是否正确!')
                return ''
        except Exception as _:
            print("获取容器Token失败, 请检查配置是否正确!")
            return ''

    def get_all_envs(self):
        """
        :return:
        """
        r = self.client.get(f'/envs')
        return r.json().get('data', [])

    def get_wp_token_by_pt_pin(self, pt_pin=None):
        if not pt_pin:
            return None
        envs = self.get_all_envs()
        for env in envs:
            if pt_pin in env['value']:
                if not env['remarks']:
                    return None
                data = env['remarks'].split('@@')
                if len(data) != 3:
                    return None
                return data[-1]

    def get_all_jd_ck(self):
        """
        :return:
        """
        cks = _get_all_jd_ck_from_env()
        if not cks:
            cks = self._get_all_jd_ck_from_api()

        return cks

    def _get_all_jd_ck_from_api(self):
        cks = []
        envs = self.get_all_envs()
        for env in envs:
            if env['name'] == 'JD_COOKIE' and env['status'] == 0:
                cks.append(env['value'])
        return cks

    def get_wp_token(self, pt_pin):
        """
        根据pt_pin查找uid token.
        :param pt_pin:
        :return:
        """
        envs = self.get_all_envs()
        for env in envs:
            if pt_pin in unquote(env['value']) and env['status'] == 0:
                if 'UID' in env['remarks']:
                    return env['remarks'].split('@@')[-1]
        return None


ct = CT()


if __name__ == '__main__':
    print(ct.get_wp_token_by_pt_pin('jd_588'))
