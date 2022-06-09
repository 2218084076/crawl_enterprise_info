"""main"""
import asyncio
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


async def all_category_to_redis():
    city_category_list = await crawl_city_category()
    for city in city_category_list:
        logging.debug('<%s> save %s' % (city, settings.get('city_redis_name')))
        save_redis(settings.get('city_redis_name'), city)


async def main_category_tesk():
    """
    category
    :return:
    """
    city_category_list = read_redis_list('city_category')
    await crawl_main_category_url(city_category_list)
    logging.debug('Complete main category')


async def detailed_category_task():
    main_category = await read_redis_list('main_category_urls')
    await crawl_detailed_category(main_category)
    logging.debug('complete detailed category')


async def company_link_task():
    detailed_category = await read_redis_list('detailed_category')
    for url in detailed_category:
        if 'http' not in url:
            url = 'https:' + url
            await crawl_company_link(url)
            logging.debug('%s save detailed_category' % url)


async def parse_task():
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


async def rollback_task():
    rollback_company = read_redis_list(settings.get('rollback'))
    for url in rollback_company:
        company_info = parse_company_info(url)
        init_mongo(company_info)


async def main():
    """
    main
    :return:
    """
    # await all_category_to_redis()
    await main_category_tesk()
    await detailed_category_task()
    await company_link_task()
    await parse_task()
    await rollback_task()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
