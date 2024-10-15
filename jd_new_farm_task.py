"""
/**
 * name: 新东东农场任务(暂不可用)
 * desc: # 并发数 JY_JD_FARM_TASK_CONC_NUM=1
 * cron: 7 7 7 7 7
 */
"""
import asyncio
import base64
import httpx
from conf import config
from utils.coroutines import start, async_print
from utils.proxy import get_proxies
from utils.new_farm import JdFarm, UA

RETRY_DELAY = int(config.JY_JD_FARM_WATER_RETRY_DELAY)
MAX_RETRIES = int(config.JY_JD_FARM_WATER_RETRY_NUM)


async def init_farm(**kwargs):
    """
    :return:
    """
    params = await JdFarm.create_params('farm_home', {"version": 7, "channelParam": "1"}, kwargs.get('pin'))
    url = 'https://api.m.jd.com/client.action'
    data = await JdFarm.post(url, params, **kwargs)
    if data.get('code') != 0:
        await async_print(f"进入农场首页失败, {data['msg']}")
        return False
    data = data['data']
    if data.get('bizCode') != 0:
        await async_print(f"进入农场首页失败, {data['bizMsg']}")
        return False
    data = data['result']
    invite_code = data['farmHomeShare']['inviteCode']
    water_tips = data['waterTips']
    bottle_water = data['bottleWater']
    await async_print(f"当前种植进度为: {water_tips}")
    await async_print(f"助力码为: {invite_code}")
    await async_print(f"当前剩余水滴{bottle_water}g!")

    return True


async def plant_tree(**kwargs):
    params = await JdFarm.create_params('farm_plant_tree', {"version": 7, "channelParam": "1", "uid": kwargs.get('uid'),
                                                            "type": "plantSku"}, kwargs.get('pin'))
    url = 'https://api.m.jd.com/client.action'
    return await JdFarm.post(url, params, **kwargs)


async def get_task_list(**kwargs):
    params = await JdFarm.create_params('farm_task_list',
                                        {"version": 7, "channelParam": "1", "channel": 0, "babelChannel": "ttt7",
                                         "lbsSwitch": True},
                                        kwargs.get('pin'))
    url = 'https://api.m.jd.com/client.action'
    data = await JdFarm.post(url, params, **kwargs)
    if data.get('code') != 0:
        await async_print(f"获取任务列表失败, {data['msg']}")
        return []

    data = data['data']
    if data.get('bizCode') != 0:
        await async_print(f'获取任务列表失败, {data["bizMsg"]}')
        return []

    return data['result']['taskList']


async def get_task_detail(task, **kwargs):
    body = {
        "version": 7,
        "channelParam": "1",
        "taskType": task['taskType'],
        "taskId": task['taskId'],
        "channel": 0
    }
    params = await JdFarm.create_params('farm_task_detail',
                                        body,
                                        kwargs.get('pin'))
    url = 'https://api.m.jd.com/client.action'
    data = await JdFarm.post(url, params, **kwargs)
    if data.get('code') != 0:
        await async_print(F'获取任务《{task["mainTitle"]}》详细信息失败!')
        return None

    data = data['data']
    if data.get('bizCode') != 0:
        await async_print(F'获取任务《{task["mainTitle"]}》详细信息失败, {data["bizMsg"]}')
        return

    return data['result']['taskDetaiList']


async def do_task(task, **kwargs):
    item_id = task.get('taskSourceUrl', '')
    task_insert = False
    if not item_id:
        task_detail = await get_task_detail(task, **kwargs)
        if not task_detail:
            return
        print(task_detail)
        item_id = task_detail[0].get('itemId', task_detail[0].get('itemUrl', ''))
        task_insert = task_detail[0].get('taskInsert', False)
        print(task_detail)
    print(item_id)
    item_id = base64.b64encode(item_id.encode('utf8')).decode('utf8')

    body = {
        "version": 7,
        "channelParam": "1",
        "taskType": task['taskType'],
        "taskId": task['taskId'],
        "taskInsert": task_insert,
        "itemId": item_id,
        "channel": 0
    }
    print(body)
    params = await JdFarm.create_params('farm_do_task',
                                        body,
                                        kwargs.get('pin'), h5st_template='20241011164259781;z93z9p9ztwim9zw2;28981;tk03wd1551d1118nQjSunVKcehws7MtbWYJZ8S5B0MZmvujkGT-wjZX5voTSRyE99rKmbHECZqW1y-riQjffcDeirVMA;fde86a329a164268a0e5f8dd6dc767449ba62935efab07be1a38efc6bca692a3;4.2;1728636179781;e9f6ec1bab0ebf8ad0759c5c9ae319e1030045229d00313e52233354c9b748d440890c4e82bfeb1b5affb9c351b4b40255de0468a9ba0782ea6005d65e47c3ce1a9b08cf55d1d79918f718a4d22b7c657560901895d4b32bfcb185941d63f21779315a9be7a949d4dc391c848e49e4aef8cfa80c941788e87d5c0b051ece05a6af1e9f5dc38d7047cf9caa4fe452a916122197a08b009a693f78df6ad6b9eda5808905df82ca88b3a489b5986fdb9ef36b83200219399783a2976ecf86b363cc2dda0d716e4df2490e3ead7a6d04f220f7cac27c59f707c5c2ea98dcbdd51772e063da5cb8605e117216e9555dd291a250da74d0d5d5ebba0180334abed0cc70f6b632bd9559859946d008b0619e82a1363a172c0b92d6efc9c566ae691ad1b22b6e88db83689c7802ec1c3acf6f0c4b')
    url = 'https://api.m.jd.com/client.action'
    data = await JdFarm.post(url, params, **kwargs)
    print(data)


async def jd_farm_task(jd_ck, **kwargs):
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
        if not await init_farm(**kwargs):
            return

        task_list = await get_task_list(**kwargs)
        if not task_list:
            return

        for task in task_list:
            task_type = task['taskType']
            task_status = task['taskStatus']
            task_title = task['mainTitle']

            if task_type in ['ORDER_MARK']:
                continue

            if task_status == 3:
                await async_print(f'任务《{task_title}》奖励已领取!')
                continue

            if task_status == 2:
                await async_print(f'任务《{task_title}》已完成!')
                continue

            if task_type in ['CUMULATIVE_TIMES']:
                continue

            await do_task(task, **kwargs)
            await asyncio.sleep(2)
            print(task_type)
            # body = {
            #     "version": 7,
            #     "channelParam": "1",
            #     "taskType": task_type,
            #     "taskId": 6689,
            #     "taskInsert": False,
            #     "itemId": "aHR0cHM6Ly9wcm8ubS5qZC5jb20vbWFsbC9hY3RpdmUvMkF0V1QzblVzWUt0OXVYeWNQVk1HOFhBTTlmQS9pbmRleC5odG1sP3NpdGVDbGllbnQ9d2g1JnNpdGVDbGllbnRWZXJzaW9uPTIuMC4wJnRhYklkPTEmc3ViVGFiVHlwZT0xJnF1ZXJ5VHlwZT0xJnBhZ2VOdW09MSZ0YWJUeXBlPTEmdHJhbnNwYXJlbnQ9MSZiYWJlbENoYW5uZWw9dHR0Mg==",
            #     "channel": 0
            # }
            # data = await do_task()


if __name__ == '__main__':
    pass
    # start(jd_farm_task, '新东东农场任务')
