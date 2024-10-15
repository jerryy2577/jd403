import asyncio
from utils.ct import ct
from utils.com import unquote_pt_pin, match_value_from_cookie
from conf import config

async def async_print(*args, **kwargs):
    print(asyncio.current_task().get_name() + ':', *args,  **kwargs)


async def limited_run(semaphore, func, jd_ck, **kwargs):
    async with semaphore:
        return await func(jd_ck, **kwargs)


async def async_run(func: callable, name='任务', max_concurrent=1, **kwargs):
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = []
    jd_cks = ct.get_all_jd_ck()
    is_print_msg = kwargs.get('is_print_msg', True)
    if is_print_msg:
        print(f'开始任务:《{name}》'.rjust(30, '<').ljust(56, '>'))
        print("""
        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            有问题先更新, 请关注频道或进群反馈!
            仓库: https://github.com/jerryy2577/jd403
            频道: https://t.me/jd403ya
            群组: https://t.me/jd403la
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            """)
        print('\n===========当前使用代理池:{}===========\n'.format(config.JY_PROXY_POOL))
    for i in range(len(jd_cks)):
        jd_ck = jd_cks[i]
        pt_pin = match_value_from_cookie(jd_ck)
        kwargs.update({
            'pin': pt_pin
        })
        task = asyncio.create_task(limited_run(semaphore, func, jd_ck, **kwargs))
        task.set_name('账号{}-{}'.format(i + 1, unquote_pt_pin(pt_pin)))
        tasks.append(task)
    await asyncio.gather(*tasks)

    print(f'结束任务《{name}》'.rjust(30, '<').ljust(56, '>'))


def start(func: callable, name='新东东', max_concurrent=1, **kwargs):
    asyncio.run(async_run(func, name, max_concurrent, **kwargs))

