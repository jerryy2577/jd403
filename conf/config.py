import os
import shutil
from collections import OrderedDict

from dotenv import dotenv_values

class Config:

    def __init__(self):
        self.JY_REDIS_PWD = None
        self.JY_REDIS_PORT = None
        self.JY_REDIS_HOST = None
        self.JY_SIGN_URL = None
        self.JY_H5ST_URL = None
        self.JY_PROXY_POOL = None
        self.JY_CT_CLIENT_SECRET = None
        self.JY_CT_CLIENT_ID = None
        self.JY_CT_URL = None
        self.JY_JD_FARM_WATER_RETRY_NUM = None
        self.JY_JD_FARM_WATER_RETRY_DELAY = None
        self.JY_JD_FARM_QUERY_AWARD_CONC_NUM = None
        self.JY_JD_FARM_WATER_CONC_NUM = None
        self.JY_JD_FARM_TASK_CONC_NUM = None
        self.JY_JD_WYW_EXCHANGE_CONC = None
        self.JY_JD_WYW_EXCHANGE_AWARD = None

    def set(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get(self, key, default=None):
        return getattr(self, key, default)


def find_project_root():
    """
    :return:
    """
    current_path = os.getcwd()
    while current_path != os.path.dirname(current_path):
        if 'notify.py' in os.listdir(current_path) or 'conf' in os.listdir(current_path):
            return current_path
        current_path = os.path.dirname(current_path)
    return None


def load_dotenv(base_dir):
    """
    :param base_dir:
    :return:
    """
    env_path = os.path.join(base_dir, '.env')
    env_example_path = os.path.join(base_dir, '.env.example')
    if not os.path.exists(env_path):
        shutil.copy(env_example_path, env_path)
    values = dotenv_values(env_path)
    return values


BASE_DIR = find_project_root()
config = Config()

# 数据目录
LOG_DIR = os.path.join(BASE_DIR, 'storage', 'data')
os.makedirs(LOG_DIR, exist_ok=True)
config.set(LOG_DIR=LOG_DIR)

# 日志目录
LOG_DIR = os.path.join(BASE_DIR, 'storage', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
config.set(LOG_DIR=LOG_DIR)

# 缓存目录
CACHE_DIR = os.path.join(BASE_DIR, 'storage', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)
config.set(CACHE_DIR=CACHE_DIR)

# 模板目录
CACHE_DIR = os.path.join(BASE_DIR, 'storage', 'template')
os.makedirs(CACHE_DIR, exist_ok=True)
config.set(CACHE_DIR=CACHE_DIR)

config.set(**load_dotenv(BASE_DIR))


if __name__ == '__main__':
    pass

