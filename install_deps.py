"""
/**
 * name: 一键初始化配置和安装依赖
 * desc: 新东东农场浇水默认浇完所有水滴
 * cron: 7 7 7 7 7
 */
"""
import os.path
import sys
import requests

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

ENV_FILE_DOWNLOAD_URL = 'https://raw.githubusercontent.com/jerryy2577/jd403/refs/heads/main/.env.example'

DEPENDENCIES_FILE_DOWNLOAD_URL = 'https://raw.githubusercontent.com/jerryy2577/jd403/refs/heads/main/requirements.txt'

REQUIREMENTS_FILENAME = 'requirements.txt'


def install_dependencies():
    env_path = os.path.join(BASE_DIR, '.env')
    if not os.path.exists(env_path):
        print('环境变量配置文件.env不存在, 开始下载!')
        result = download(ENV_FILE_DOWNLOAD_URL, env_path)
        if result:
            print('成功下载环境变量配置文件.env!')
        else:
            print('未能成功下载环境变量配置文件.env, 请检查当前网络是否能够正常访问github.com!')

    dependencies_path = os.path.join(BASE_DIR, REQUIREMENTS_FILENAME)
    result = download(DEPENDENCIES_FILE_DOWNLOAD_URL, dependencies_path)
    if not result:
        print('未能成功下载依赖配置文件, 请检查当前网络是否能够正常访问github.com!')
        return

    print('开始安装依赖...')
    os.system(f'pip install --upgrade pip')
    os.system(f'pip install -r {dependencies_path}')
    print('依赖安装结束...')


def download(url, path):
    try:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/105.0.0.0 Safari/537.36'
        }
        with requests.get(url, stream=True, headers=headers) as r:
            r.raise_for_status()
            with open(path, 'wb') as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(e.args)
        return False


if __name__ == '__main__':
    install_dependencies()
