"""category urls redis"""
import redis

redis_content = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def city_category_save_redis(category_url: str):
    """
    category url save to redis
    init redis port:6379
    :param category_url:
    """

    redis_content.lpush('category_urls', category_url)


def read_city_list() -> list:
    """
    read city category list
    :return:
    """
    end_num = redis_content.llen('category_urls')
    city_list = redis_content.lrange('category_urls', 0, end_num)

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
