# -*- coding: utf-8 -*- 
LIMITER_CONFIG = {
    'Binance':{
        'rate': {
            'ETH/BTC': 1,
            'default': 1
        },
        'max_concurrent': 20
    }
}

REDIS_CONFIG = {
    "url": "redis://127.0.0.1:6379/1"
}

IP_CONFIG = {
    'ip_list':[],  # 可用ip列表
    'ip_retry_interval':60,  # ip封禁多久后，可参与测试重用
    'reuse_ip_count': 1000,  # 访问了多少次url后，检测禁用ip是否可以
    "Binance_test_url": ""  # 测试IP是否可用的地址
}

DATA_ERROR_CONFIG = {
    "Binance":{
        "code": [1053, "IP_BAN"]
    }
}
