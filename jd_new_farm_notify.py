"""
/**
 * name: 缓存Token
 * cron: 7 7 7 7 7
 */
"""
import httpx
from conf import config
from utils.coroutines import start, async_print
from utils.proxy import get_proxies
from utils.jd_farm import JdFarm, UA
from utils.com import unquote_pt_pin, match_value_from_cookie
from utils.ct import ct
from utils.push import wp_push


async def query_award(**kwargs):
    params = await JdFarm.create_params('farm_award_detail', {"version": 5, "type": 1}, kwargs.get('pin'))
    url = 'https://api.m.jd.com/client.action'
    return await JdFarm.post(url, params, **kwargs)


async def jd_new_farm_notify(jd_ck, **kwargs):
    """
    :return:
    """
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': UA,
        'x-referer-page': 'https://h5.m.jd.com/pb/015686010/Bc9WX7MpCW7nW9QjZ5N3fFeJXMH/index.html',
        'origin': 'https://h5.m.jd.com/',
        'referer': 'https://h5.m.jd.com/',
        'cookie': jd_ck,
    }
    async with httpx.AsyncClient(proxies=get_proxies(), headers=headers) as client:
        notify_msg = ''
        pt_pin = unquote_pt_pin(match_value_from_cookie(jd_ck))

        kwargs.setdefault('client', client)
        data = await query_award(**kwargs)
        if data.get('code') != 0 or data.get('data').get('bizCode') != 0:
            await async_print("查询奖品失败, {}".format(data.get('data', {}).get('bizMsg', '原因未知')))
            return

        award_list = data.get('data').get('result').get('plantAwards')
        if not award_list:
            await async_print("当前暂无奖品!")
            return

        for award in award_list:
            if award['awardStatus'] == 1:   # 奖品未领取
                exchange_remind = award['exchangeRemind']
                notify_msg += (f'- 账号:{pt_pin}种植的水果奖励实物卷, {exchange_remind}'
                               f'请尽快去京东APP中使用~\n **奖品兑换入口: 我的->东东农场->记录(在左上角)**')
                break

        if not notify_msg:
            await async_print("当前暂无奖品")
            return

        uid = ct.get_wp_token(pt_pin)
        if not uid:
            await async_print(notify_msg)
            await async_print("===未找到用户的UID, 不发送通知===")
            return

        await async_print(notify_msg)
        await wp_push(uid, '你就好啦, 农场又可以领啦!', notify_msg)


if __name__ == '__main__':
    start(jd_new_farm_notify, '新东东农场奖品通知', max_concurrent=int(config.JY_JD_FARM_QUERY_AWARD_CONC_NUM))
