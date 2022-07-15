"""
category urls redis
添加open close操作
"""
import hashlib
import logging

import redis

logger = logging.getLogger(__name__)


# pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
# redis_content = redis.Redis(connection_pool=pool)


class RedisBase:
    """Redis Base"""

    host = 'localhost'
    port = 6379
    db = 0
    decode_responses = True

    def __init__(self):
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db,
                                         decode_responses=self.decode_responses)
        self.redis_content = redis.Redis(connection_pool=self.pool)

    def add_url(self, url: str):
        """
        add_url
        :param url:
        :return:
        """
        res = self.redis_content.sadd('key', get_md5(url))

        if res == 0:
            return False

        return True

    def save_redis(self, key: str, value: str):
        """
        save_redis
        :param key:
        :param value:
        :return:
        """
        if self.add_url(value):
            self.redis_content.lpush(key, value)

        else:
            pass

    def read_redis(self, key: str):
        """
        read_redis
        :param key:
        :return:
        """
        end_num = self.redis_content.llen(key)
        content = self.redis_content.lrange(key, 0, end_num)
        return content


def get_md5(val):
    """
    把目标数据进行哈希，用哈希值去重更快
    :param val:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(val.encode('utf-8'))
    return md5.hexdigest()
