import random



def get_device():
    """
    """
    devices = {
        'OnePlus': [
            'HD1900', 'HD1901', 'HD1907', 'HD1910', 'HD1911',
            'HD1913', 'HD1925', 'IN2010', 'IN2017', 'IN2020', 'KB2000', 'KB2001',
            'KB2007', 'LE2100', 'LE2110', 'LE2117', 'MT2110', 'NE2210', 'PGKM10',
            'PGZ110', 'PGP110', 'PHB110', 'PHK110', 'PHP110', 'PJD110', 'PJE110',
            'PJF110', 'PJZ110', 'DN2101', 'CPH2399', 'CPH2551',
        ],
        "realme":  [
            "RMX3995", "RMX3996", "RMX1991", "RMX1931", "RMX2051",
            "RMX2025", "RMX2071", "RMX2072", "RMX2141", "RMX2142",
            "RMX2052", "RMX2176", "RMX2121", "RMX3115", "RMX3116",
            "RMX2202", "RMX3361", "RMX3366", "RMX3310", "RMX3300",
            "RMX3551", "RMX3820", "RMX3823", "RMX3888", "RMX3800",
            "RMX3031", "RMX3350", "RMX3370", "RMX3357", "RMX3560",
            "RMX3562", "RMX3706", "RMX3708", "RMX3700", "RMX3852",
            "RMX3850", "RMX1971", "RMX2117", "RMX2173", "RMX2200",
            "RMX3161", "RMX2205", "RMX3142", "RMX3042", "RMX3461",
            "RMX3462", "RMX3478", "RMX3372", "RMX3574", "RMX3616",
            "RMX3615", "RMX3617", "RMX3663", "RMX3687", "RMX3751",
            "RMX3770", "RMX3740", "RMX3992", "RMX3993", "RMX3843",
            "RMX3841", "RMX3952", "RMX5002", "RMX3989", "RMX3920",
            "RMX2200", "RMX2201", "RMX2111", "RMX2112", "RMX3121",
            "RMX3122", "RMX3125", "RMX3041", "RMX3043", "RMX3092",
            "RMX3093", "RMX3610", "RMX3611", "RMX3571", "RMX3576",
            "RMX3475", "RMX3619", "RMX3618", "RMX3783", "RMX3781",
        ],
        "Xiaomi": [
            "M2002J9E", "M2002J9G", "M2002J9S",
            "M2002J9R", "M2007J1SC", "M2007J3SY",
            "M2007J3SP", "M2007J3SG", "M2007J3SI",
            "M2007J17G", "M2007J17I", "M2102J2SC",
            "M2102K1C", "M2102K1G", "M2101K9C",
            "M2101K9G", "M2101K9R", "M2101K9AG",
            "M2101K9AI", "2107119DC", "2109119DG",
            "2109119DI", "M2012K11G", "M2012K11AI",
            "M2012K11I", "21081111RG", "2107113SG",
            "2107113SI", "2107113SR", "21091116I",
            "21091116UI", "2201123C", "2201123G",
            "2112123AC", "2112123AG", "2201122C",
            "2201122G", "2207122MC", "2203129G",
            "2203129I", "2206123SC", "2206122SC",
            "2203121C", "22071212AG", "22081212UG",
            "22081212R", "22200414R", "A201XM",
            "2211133C", "2211133G", "2210132C",
            "2210132G", "2304FPN6DC", "2304FPN6DG",
            "2210129SG", "2306EPN60G", "2306EPN60R",
            "XIG04", "23078PND5G", "23088PND5R",
            "A301XM", "23127PN0CC", "23127PN0CG",
            "23116PN5BC", "2311BPN23C", "24031PN0DC",
            "24030PN60G", "24053PY09I", "2406APNFAG",
            "XIG06", "2407FPN8EG", "2407FPN8ER",
        ]
    }
    device_brand = random.choice(list(devices.keys()))
    return device_brand, random.choice(devices[device_brand])


def get_random_uuid():
    return f"{''.join(random.choices('123456789', k=16))}-{''.join(random.choices('0123456789', k=16))}"


if __name__ == '__main__':
    print(get_devices())