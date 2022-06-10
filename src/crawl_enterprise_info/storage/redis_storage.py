"""category urls redis"""
import redis

redis_content = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def save_redis(name, category_url: str):
    """
    category url save to redis
    init redis port:6379
    :param name:
    :param category_url:
    """
    redis_content.lpush(name, category_url)


def read_redis_list(name: str) -> list:
    """
    read redis
    :return:
    """
    end_num = redis_content.llen(name)
    content_list = redis_content.lrange(name, 0, end_num)

    return content_list


def main_category_url_redis(main_category_url: str):
    """
    main category url redis
    :param main_category_url:
    :return:
    """
    redis_content.lpush('main_category_urls', main_category_url)
