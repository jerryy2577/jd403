import httpx
from conf import config
from utils.proxy import get_no_proxies
from utils.coroutines import async_print


async def wp_push(uid, title='', msg=''):
    """
    :param uid:
    :param title:
    :param msg:
    :return:
    """
    try:
        url = 'https://wxpusher.zjiecode.com/api/send/message'
        data = {
            "appToken": config.JY_WP_APP_TOKEN_ONE,
            "content": msg,
            "summary": title,
            "uids": [
                uid,
            ],
            "contentType": 3
        }
        async with httpx.AsyncClient(proxies=get_no_proxies()) as client:
            response = await client.post(url, json=data)
            data = response.json()
            if data.get('code') == 1000:
                await async_print('wp_push成功发送消息!')
            else:
                await async_print('wp_push发送消息失败, {}'.format(data.get('msg')))
    except Exception as e:
        await async_print('wp_push发送消息失败, {}'.format(e.args))
        return False
