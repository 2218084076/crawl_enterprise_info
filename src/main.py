"""main"""
import logging

from crawl_enterprise_info.config import settings
from crawl_enterprise_info.crawl import (crawl_city_category,
                                         crawl_company_link,
                                         crawl_detailed_category,
                                         crawl_main_category_url,
                                         parse_company_info)
from crawl_enterprise_info.storage.mongodb_storage import init_mongo
from crawl_enterprise_info.storage.redis_storage import (read_redis_list,
                                                         save_redis)

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s - %(funcName)s')


def all_category_to_redis():
    city_category_list = crawl_city_category()
    for city in city_category_list:
        logging.debug('<%s> save %s' % (city, settings.get('city_redis_name')))
        save_redis(settings.get('city_redis_name'), city)


def category():
    """
    category
    :return:
    """
    city_category_list = read_redis_list('city_category')
    crawl_main_category_url(city_category_list)
    logging.debug('Complete main category')


def detailed_category_task():
    main_category = read_redis_list('main_category_urls')
    crawl_detailed_category(main_category)
    logging.debug('complete detailed category')


def company_link_task():
    detailed_category = read_redis_list('detailed_category')
    for url in detailed_category:
        if 'http' not in url:
            url = 'https:' + url
            crawl_company_link(url)
            logging.debug('%s save detailed_category' % url)


def parse_task():
    """
    parsing tasks
    :return:
    """
    company_urls = read_redis_list(settings.get('company_redis_name'))
    for url in company_urls:
        company_info = parse_company_info(url)
        logging.debug('Get %s company_info %s ' % (url, company_info))
        if company_info:
            init_mongo(company_info)


def rollback_task():
    rollback_company = read_redis_list(settings.get('rollback'))
    for url in rollback_company:
        company_info = parse_company_info(url)
        init_mongo(company_info)


def main():
    """
    main
    :return:
    """
    # all_category_to_redis()
    # category()
    # detailed_category_task()
    # company_link_task()
    parse_task()
    rollback_task()


if __name__ == '__main__':
    main()
