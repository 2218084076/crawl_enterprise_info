"""
category urls redis
添加open close操作
"""
import hashlib
import logging

import redis

logging.basicConfig(filename='example.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s - %(funcName)s - %(lineno)d: ',
                    )
pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
redis_content = redis.Redis(connection_pool=pool)


def get_md5(val):
    """
    把目标数据进行哈希，用哈希值去重更快
    :param val:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(val.encode('utf-8'))
    return md5.hexdigest()


def add_url(url: str) -> bool:
    """
    添加redis验证是否唯一
    :param key:
    :param url:
    :return:
    """
    res = redis_content.sadd('key', get_md5(url))  # 保存set
    if res == 0:  # 若返回0,说明插入不成功，表示有重复
        return False
    else:
        return True


def save_redis(key: str, value: str):
    """
    save set
    :param key:
    :param value:
    :return:
    """
    if add_url(value):
        redis_content.lpush(key, value)
        logging.debug('save %s %s' % (key, value))
    else:
        pass


def read_redis(key: str):
    """
    read set
    :param key:
    :return:
    """
    end_num = redis_content.llen(key)
    content = redis_content.lrange(key, 0, end_num)
    logging.debug('redis %s content is %s' % (key, content))
    return content


def close_redis():
    """
    close redis
    :return:
    """