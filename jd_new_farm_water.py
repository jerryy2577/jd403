"""
/**
 * name: 新东东农场浇水
 * desc: 新东东农场浇水默认浇完所有水滴
         # 并发浇水
         JY_JD_FARM_WATER_CONC_NUM=1
 * cron: 35 7,21 * * *
 */
"""
import asyncio
import random
import httpx
from conf import config
from utils.coroutines import start, async_print
from utils.proxy import get_proxies
from utils.new_farm import JdFarm, UA

RETRY_DELAY = int(config.JY_JD_FARM_WATER_RETRY_DELAY)
MAX_RETRIES = int(config.JY_JD_FARM_WATER_RETRY_NUM)
H5ST_TEMPLATE = '20241011155136324;z93z9p9ztwim9zw2;28981;tk03wd1551d1118nQjSunVKcehws7MtbWYJZ8S5B0MZmvujkGT-wjZX5voTSRyE99rKmbHECZqW1y-riQjffcDeirVMA;64c3737ab76089fa7ce780cbcb5db873eadfc6bc853ef716bb68966078c19cb6;4.2;1728633096324;e9f6ec1bab0ebf8ad0759c5c9ae319e1030045229d00313e52233354c9b748d440890c4e82bfeb1b5affb9c351b4b40255de0468a9ba0782ea6005d65e47c3ce1a9b08cf55d1d79918f718a4d22b7c657560901895d4b32bfcb185941d63f21779315a9be7a949d4dc391c848e49e4aef8cfa80c941788e87d5c0b051ece05a6af1e9f5dc38d7047cf9caa4fe452a916122197a08b009a693f78df6ad6b9eda5808905df82ca88b3a489b5986fdb9ef36b83200219399783a2976ecf86b363cc2dda0d716e4df2490e3ead7a6d04f22003b85bec4c187847d0514e86e7f6a2fc435a42bc55b4bb502ddadd99b2eeffb259e8131d7572ebec7a7b567a5b5e07e54890f81c9cac841751e982589ce266bcd9cb46808e5e09c05ab38d8e898f911a378631798311ed9fe09031f917482fab'


async def watering(**kwargs):
    params = await JdFarm.create_params('farm_water',
                                        {"version": 7, "channelParam": "1", "waterType": 1, "babelChannel": "ttt7",
                                         "lbsSwitch": True}, kwargs.get('pin'), H5ST_TEMPLATE)
    url = 'https://api.m.jd.com/client.action'
    return await JdFarm.post(url, params, **kwargs)


async def watering_n_times(**kwargs):
    """
    """
    attempt = 0
    bottle_water = kwargs.get('bottle_water', 0)
    water_num = kwargs.get('water_num')
    if bottle_water < 10:
        return await async_print('当前剩余水滴不足10g, 停止浇水!')

    while bottle_water > 0:
        if attempt >= MAX_RETRIES:
            return await async_print('浇水错误达到最大重试次数, 不再浇水!')
        data = await watering(**kwargs)
        if data['code'] != 0:
            return await async_print(data.get('msg', '浇水异常'))
        data = data['data']
        match data['bizCode']:
            case 0:
                data = data['result']
                bottle_water = int(data['bottleWater'])
                water_tips = data['waterTips']
                await async_print(f'浇水成功, {water_tips}, 剩余水滴{bottle_water}g!')
            case 4:
                await async_print(data.get('bizMsg', '没有水滴了, 浇个锤子！'))
                break
            case -1001:
                msg = data.get('bizMsg', '活动火爆, 估计是个黑子!')
                await async_print(f'浇水失败, {msg}, 等到{RETRY_DELAY}秒后重试!')
                attempt += 1
                await asyncio.sleep(RETRY_DELAY)
            case _:
                err_msg = data.get('bizMsg', '未知!')
                await async_print(f'浇水失败, {err_msg}')
                break
        await asyncio.sleep(random.randint(2, 5) / 10)

    await async_print('当前总共浇水{}次!'.format(water_num))


async def jd_farm_water(jd_ck, **kwargs):
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
        kwargs.setdefault('client', client)
        data = await watering(**kwargs)
        if data['code'] != 0:
            return await async_print(data.get('msg', '浇水异常'))
        data = data['data']

        match data['bizCode']:
            case 0:
                bottle_water = int(data['result']['bottleWater'])
                kwargs.setdefault('bottle_water', bottle_water)
                kwargs.setdefault('water_num', 1)
                return await watering_n_times(**kwargs)
            case 4:
                return await async_print(data.get('bizMsg', '没有水滴了, 浇个锤子！'))
            case -1001:
                return await async_print(data.get('bizMsg', '活动火爆, 估计是个黑子!'))
            case _:
                err_msg = data.get('bizMsg', '未知!')
                return async_print(f'浇水失败, {err_msg}')


if __name__ == '__main__':
    start(jd_farm_water, '新东东农场浇水', max_concurrent=int(config.JY_JD_FARM_WATER_CONC_NUM))
