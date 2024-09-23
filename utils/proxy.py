from conf import config


def get_proxies():
    """
    :return:
    """
    if config.JY_PROXY_POOL:
        proxies = {'all://': config.JY_PROXY_POOL}
    else:
        print('环境变量:JY_PROXY_POOL未配置, 不使用代理!')
        return get_no_proxies()
    return proxies


def get_no_proxies():
    """
    :return:
    """
    return {'all://': None}


if __name__ == '__main__':
    print(get_proxies())
    print(get_no_proxies())