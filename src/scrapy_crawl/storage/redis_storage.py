"""category urls redis"""
import redis

redis_content = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


class LinkRedis(object):

    def __init__(self, host='localhost', port=6379, db=0, decode_responses=True):
        """
        初始化Redis连接池
        :param host: 主机名
        :param port: 端口
        :param db: 数据库
        """
        pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            max_connections=None
        )
        self.redis = redis.Redis(connection_pool=pool)

    def __del__(self):
        """
        任务结束后关闭连接
        :return:
        """
        self.redis.connection_pool.disconnect()

    def exists(self, name):
        """
        检查name是否存在
        :param name:
        :return:
        """

        return self.redis.exists(name)

    def delete(self, name):
        """
        删除指定name
        :param name:
        :return:
        """

        return self.redis.delete(name)

    def add_redis(self, value):
        """
        add redis
        :param value:
        :return:
        """
        self.redis.lpush(value)


def category_save_redis(name, category_url: str):
    """
    category url save to redis
    init redis port:6379
    :param name:
    :param category_url:
    """

    redis_content.lpush(name, category_url)


def read_redis_list(name) -> list:
    """
    read city category list
    :return:
    """
    end_num = redis_content.llen(name)
    city_list = redis_content.lrange(name, 0, end_num)

    return city_list


def main_category_url_redis(main_category_url: str):
    """
    main category url redis
    :param main_category_url:
    :return:
    """

    redis_content.lpush('main_category_urls', main_category_url)


def company_link_redis():
    """"""
