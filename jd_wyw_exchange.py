"""
/**
 * name: 玩一玩兑换奖品
 * desc: 设置需要兑换的奖品名称, 多个奖品用&分隔,如:   JY_JD_WYW_EXCHANGE_AWARD='50京豆&10元红包'
         设置同时执行的账号数量, JY_JD_WYW_EXCHANGE_CONC=2
 * cron: 0 */2 * * *
 */
"""
import asyncio
import random
import sys
import httpx
from conf import config
from utils.coroutines import start, async_print
from utils.proxy import get_proxies
from utils.wyw import UA, JdWyw
from utils.ct import ct


async def get_exchange_info():
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': UA,
        'x-rp-client': 'h5_1.0.0',
        'x-referer-page': 'https://pro.m.jd.com/mall/active/3aydrBPrN7xsUGwj31PK3UhkHAqA/index.html',
        'referer': 'https://pro.m.jd.com/mall/active/3aydrBPrN7xsUGwj31PK3UhkHAqA/index.html',
        'origin': 'https://pro.m.jd.com',
        'x-requested-with': 'com.jingdong.app.mall',
        'cookie': random.choice(ct.get_all_jd_ck())
    }
    async with httpx.AsyncClient(proxies=get_proxies(), headers=headers, http2=True) as client:
        params = await JdWyw.create_params('wanyiwan_exchange_page', {"showShortcut": True, "version": 7}, '随便啦')
        url = 'https://api.m.jd.com/client.action'
        return await JdWyw.post(url, params, client=client)


async def wyw_exchange(body, **kwargs):
    params = await JdWyw.create_params('wanyiwan_exchange', body, kwargs.get('pin'),
                                       '20241015152047024;2bdd22d2ockx1sx0;399a0;tk03wb6c91c7218nlNsyydxKaIINLK3mTUwwXP4aAZH9q7Goq69GlBVRc2YgfFYNQ8DRnrMh5YzrR2mKSIe6OEUyyCzw;21b77314fc93b29dfa2d80047286d936;4.8;1728976847024;TKmWZt2Om2f6l2f8zZwKyNzKyFw_kOUOcOU6wNUO2uWLeW0I0eg_zNUO2uWL0CA9mCz9jOwJd_QJm_w_lCA_fyTJdWDIf6D_gKT9l6TI0W0I0WvFq5w_x5vO2W0UqOU9y5j_eWj_15jKlCj_kCD9gWDJmyDKzJQIiyzJdyjJfOUOcOk619v71JwO2W0UqO0Ko2zLi_f-xlA8wZBJuNUOcO050WUOMm0OfGj_ydg9s1wGcFxO2uzOpZQ9oRw60WUOMm0Oi_T8zN-_1VU4hdA8KNUOcO09mNUO2uWLZVUOMWTOcOUIhNwO2WUO2uWL0OUOcOkJhNwO2WUO2uWLiSTOcO0JhNwO2WUO2uWLmW0I0CD50NUO2WUOMmUK2uzOiCv_0WUO2W0UqKzJ2uzOjCv_0WUO2W0UqSDL2uzOkCv_0WUO2W0UqOEJoSzLmaB9ixQ70W0I0SD50NUO2WUOMmUK2uzOr5vO2WUO2uWLmW0I0KP70WUO2W0UqWTOcOU70WUO2W0UqWTOcOU9fNUO2WUOMqPOcOU9oBQ5eBwO2W0UqiPO2u2OmthFDtSAiVP7xlg_3Fw80W0I0ST60WUO2W0UbV0I0WP60WUOMm0Og5PObSTKmekKlSDKlOzLlShEDZU9qxA5UVkKmyDKS1SObODK2GA8nNP9oRSOb2-5oxQD0W0I0SA5jNUO2um4;b14e0822e5d7c8e487f38e32aeaf438a')
    url = 'https://api.m.jd.com/client.action'
    return await JdWyw.post(url, params, **kwargs)


def get_award_list():
    data = asyncio.run(get_exchange_info())
    if data.get('code') != 0:
        print('获取奖品列表失败, 退出程序...')
        return None
    data = data['data']
    if data.get('bizCode') != 0:
        print('获取奖品列表失败:{} 退出程序...'.format(data['bizMsg']))
        return False
    data = data['result']
    print('奖品列表'.rjust(30, '<').ljust(56, '>'))
    for item in data['moreExchanges']:
        reward_name = item['rewardName'].rjust(15)
        has_stock = '有库存' if item['hasStock'] else '无库存'
        exchange_score = '兑换所需奖票: {}'.format(item['exchangeScore']).ljust(15)
        print('|{}\t|\t{}\t|\t{}\t|'.format(reward_name, has_stock, exchange_score))
    print('奖品列表'.rjust(30, '<').ljust(56, '>'))

    if not config.JY_JD_WYW_EXCHANGE_AWARD:
        print(
            '未设置兑换商品变量, 请先设置环境变量,多个商品使用&分割, 例如: JY_JD_WYW_EXCHANGE_AWARD="50京豆&10元红包"')
        sys.exit()
    print('当前设置兑换商品: {}'.format(', '.join(config.JY_JD_WYW_EXCHANGE_AWARD.split('&'))))

    return data['moreExchanges']


async def jd_wyw_exchange(jd_ck, **kwargs):
    """
    :return:
    """
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': UA,
        'x-rp-client': 'h5_1.0.0',
        'x-referer-page': 'https://pro.m.jd.com/mall/active/3aydrBPrN7xsUGwj31PK3UhkHAqA/index.html',
        'referer': 'https://pro.m.jd.com/mall/active/3aydrBPrN7xsUGwj31PK3UhkHAqA/index.html',
        'origin': 'https://pro.m.jd.com',
        'x-requested-with': 'com.jingdong.app.mall',
        'cookie': jd_ck,
    }
    async with httpx.AsyncClient(proxies=get_proxies(), headers=headers, http2=True) as client:
        kwargs.setdefault('client', client)
        awards = kwargs.get('award_list')
        exchange_award_list = sorted(config.JY_JD_WYW_EXCHANGE_AWARD.split('&'), reverse=True)

        for exchange_item in exchange_award_list:
            for award in awards:
                if exchange_item not in award['rewardName']:
                    continue

                exchange_body = {
                    "assignmentId": award['assignmentId'],
                    "type": award['rewardType'],
                    "actualExchangeScore": award['exchangeScore'],
                    "version": 7
                }
                data = await wyw_exchange(body=exchange_body, **kwargs)
                if data.get('code') != 0:  # 黑号
                    await async_print("兑换{}失败, {}".format(exchange_item, data['message']))
                    break

                data = data['data']
                if data.get('bizCode') == 0:
                    await async_print(f"成功兑换{exchange_item}!")
                else:
                    await async_print("兑换{}失败, {}".format(exchange_item, data['bizMsg']))

                await asyncio.sleep(0.5)

if __name__ == '__main__':
    award_list = get_award_list()
    start(jd_wyw_exchange, '玩一玩兑换', max_concurrent=int(config.JY_JD_FARM_WATER_CONC_NUM),
          award_list=award_list, is_print_msg=False)
