import random
from utils.devices import get_device

def get_farm_ua():

    android_versions = ['11', '12', '13', '14']

    device_model, _ = get_device()

    build_numbers = ['100007']

    template = ('jdapp;android;13.2.8;;;M/5.0;appBuild/{app_build};'
                'ef/1;;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android {android_ver};'
                ' {device_model} Build/{build_number}; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0'
                ' Chrome/{chrome_ver} MQQBrowser/6.2 TBS/046285 Mobile Safari/537.36')

    return template.format(
        app_build=random.randint(100000, 999999),
        android_ver=random.choice(android_versions),
        device_model=device_model,
        build_number=random.choice(build_numbers),
        chrome_ver=f'89.0.4389.72'
    )


if __name__ == '__main__':
    print(get_farm_ua())
