# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import re

from storage.mongodb_storage import CompanyInfoMongo
from storage.redis_storage import save_redis

logging.basicConfig(filename='example.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s - %(funcName)s - %(lineno)d: ',
                    )


def save_city_redis(city_url: str):
    """
    save_to_redis
    :param city_url:
    :return:
    """
    try:
        if '//www.11467.com' in city_url:
            if 'http' not in city_url:
                url = 'http:%s' % city_url
                save_redis('city', url)

    except Exception as e:
        logging.debug('error %s' % e)


def save_main_category(category: str):
    """
    save main category
    :param category:
    :return:
    """
    try:
        if 'https://' not in category:
            category = 'httpds://' + category
        else:
            if 'https://' in category and '.htm' in category and 'info' not in category:
                save_redis('main_category', category)

            if '//www.11467.com/' in category and 'http' not in category and '.htm' in category and category != '//www.11467.com/':
                save_company_redis(category)

    except Exception as e:
        save_detail_category(category)
        logging.debug('error %s' % e)


def save_detail_category(detail_category: str):
    """
    detail category
    :param detail_category:
    :return:
    """
    try:
        if 'https://' not in detail_category:
            detail_category = 'httpds://' + detail_category
        else:
            if re.match("^https.*.htm$", detail_category):
                save_redis('detail_category', detail_category)
            if re.match("^//b2b.*.htm$", detail_category):
                save_redis('detail_category', detail_category)
            if re.match("^http://www.11467.com", detail_category):
                save_redis('main_category', detail_category)

    except Exception as e:
        logging.debug('error %s' % e)
        save_company_redis(detail_category)


def save_company_redis(company_url: str):
    """
    save company redis
    :param company_url:
    :return:
    """
    try:
        if re.match("^//www.11467.com", company_url):
            company_url = 'https:' + company_url
            save_redis('company_links', company_url)
            if 'https:' not in company_url:
                company_url = 'https:' + company_url.group()
                save_redis('company_links', company_url)
            else:
                save_redis('company_links', company_url)

    except Exception as e:
        logging.debug('error %s' % e)


def save_company_info(company_info: dict):
    """
    save company info
    :param company_info:
    :return:
    """
    company_info_mongo = CompanyInfoMongo()
    company_info_mongo.save_company_info(company_info)


class CrawlBusinessInfoPipeline:
    """Crawl Business Info Pipeline"""

    def process_item(self, item, spider):

        if 'city_urls' in item:
            city_urls = dict(item).get('city_urls')
            for url in city_urls:
                save_city_redis(url)

        if 'main_category' in item:
            main_category = dict(item).get('main_category')
            for url in main_category:
                save_main_category(url)

        if 'detail_category' in item:
            detail_category = dict(item).get('detail_category')
            for url in detail_category:
                save_detail_category(url)

        if 'company_urls' in item:
            company_urls = dict(item).get('company_urls')
            for url in company_urls:
                save_company_redis(url)

        if 'business_model' in dict(item):
            company_info = dict(item)
            save_company_info(company_info)
