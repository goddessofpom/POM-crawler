# -*- coding: utf-8 -*- 
LIMITER_CONFIG = {
    'Binance':{
        'rate': {
            'ETH/BTC': 0.1,
            'default': 0.1
        },
        'max_concurrent': 30,
        'time_out':30
    },
    'Huobi':{
        'rate': {
            'default': 0.1
        },
        'max_concurrent': 30,
        'time_out':30
    },
    'ZB':{
        'rate': {
            'default': 0.1
        },
        'max_concurrent': 30,
        'time_out':30
    },
    'HitBTC':{
        'rate': {
            'default': 0.1
        },
        'max_concurrent': 30,
        'time_out':30
    },
    'OKEX':{
        'rate': {
            'default': 0.1
        },
        'max_concurrent': 30,
        'time_out':30
    },
    'OKCOIN':{
        'rate': {
            'default': 0.1
        },
        'max_concurrent': 30,
        'time_out':30
    },
    'Poloniex':{
        'rate': {
            'default': 0.1
        },
        'max_concurrent': 30,
        'time_out':30
    }
}

REDIS_CONFIG = {
    "host": "redis://127.0.0.1:6379",
    "db": "1"
}

MYSQL_CONFIG = {
    "min_size": 50,
    "host": "localhost",
    "user": "root",
    "passwd": "agile",
    "db": "data_service",
    "port": 3308,
    "charset": "utf8"
}

IP_CONFIG = {
    'ip_list':["192.168.199.122"],  # 可用ip列表
    'reuse_ip_count': 1000,  # 访问了多少次url后，检测禁用ip是否可以
    "Binance_test_url": "",  # 测试IP是否可用的地址
    "max_request_per_min": 60,  # 每分钟IP最大请求数
    "sleep_per_min": 1  # 每分钟请求数超过最大数后暂停的时间
}

DATA_ERROR_CONFIG = {
    "Binance":{
        "code": [-1003, "IP_BAN"]
    },
    "Huobi": {
        "status": ["error", "INVALID_PARAMETER"]
    },
    "ZB": {
    },
    "HitBTC": {
    },
    "OKEX": {
    },
    "OKCOIN": {
    },
    "Poloniex": {
    }
}

GALAXY_CONFIG = {
    "host":"https://galaxy-backup.sandyvip.com"
}

AUTH_KEY = {
    "HitBTC": {
        "KEY": ""
    }
}
