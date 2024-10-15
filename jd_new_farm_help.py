"""
/**
 * name: 新东东农场助力(暂不可用)
 * desc: 新东东农场助力
 * cron: 7 7 7 7 7
 */
"""
from conf import config
from utils.new_farm import JdFarm, UA


RETRY_DELAY = int(config.JY_JD_FARM_WATER_RETRY_DELAY)
MAX_RETRIES = int(config.JY_JD_FARM_WATER_RETRY_NUM)


async def watering(**kwargs):
    params = await JdFarm.create_params('farm_water', {"version": 5, "waterType": 1, "babelChannel": "ttt7", "lbsSwitch": False}, kwargs.get('pin'))
    url = 'https://api.m.jd.com/client.action'
    return await JdFarm.post(url, params, **kwargs)

if __name__ == '__main__':
    pass