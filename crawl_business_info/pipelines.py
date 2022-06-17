# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import re

import pymongo
from itemadapter import ItemAdapter
from scrapy import Spider

import settings
from storage.redis_storage import RedisBase

logger = logging.getLogger(__name__)


# logging.basicConfig(filename='example.log',
#                     encoding='utf-8',
#                     level=logging.DEBUG,
#                     format=' %(asctime)s - %(levelname)s - %(message)s - %(funcName)s - %(lineno)d: ',
#                     )


def save_city_redis(city_url: str):
    """
    save_to_redis
    :param city_url:
    :return:
    """
    redis_base = RedisBase()
    try:
        if '//www.11467.com' in city_url:
            if 'http' not in city_url:
                url = 'http:%s' % city_url
                redis_base.save_redis('city', url)

    except Exception as e:
        logger.info('error %s' % e)


def save_main_category(category: str):
    """
    save main category
    :param category:
    :return:
    """
    redis_base = RedisBase()
    try:
        if 'https://' not in category:
            category = 'https://' + category
        else:
            if 'https://' in category and '.htm' in category and 'info' not in category:
                redis_base.save_redis('main_category', category)

            if '//www.11467.com/' in category and 'http' not in category and '.htm' in category and category != '//www.11467.com/':
                save_company_redis(category)

    except Exception as e:
        save_detail_category(category)
        logger.info('error %s' % e)


def save_detail_category(detail_category: str):
    """
    detail category
    :param detail_category:
    :return:
    """
    redis_base = RedisBase()

    try:
        if 'https://' not in detail_category:
            detail_category = 'https://' + detail_category
        else:
            if re.match("^https.*.htm$", detail_category):
                redis_base.save_redis('detail_category', detail_category)
            if re.match("^//b2b.*.htm$", detail_category):
                redis_base.save_redis('detail_category', detail_category)
            if re.match("^http://www.11467.com", detail_category):
                redis_base.save_redis('main_category', detail_category)

    except Exception as e:
        logger.info('error %s' % e)
        save_company_redis(detail_category)


def save_company_redis(company_url: str):
    """
    save company redis
    :param company_url:
    :return:
    """
    redis_base = RedisBase()

    try:
        if '//www.11467.com' in company_url and 'b2b' not in company_url:
            company_url = 'https:' + company_url
            redis_base.save_redis('company_links', company_url)
        else:
            redis_base.save_redis('company_links', company_url)

    except Exception as e:
        logger.info('Error %s' % e)


class CrawlBusinessInfoPipeline:
    """Crawl Business Info Pipeline"""

    collection_name = settings.COLLECTIOIN_NAME

    def __init__(self, mongo_uri, mongo_db):
        self.db = None
        self.client = None
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider: Spider):
        """open spider"""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        spider.logger.info('open spider')

    def close_spider(self, spider):
        """close spider"""
        self.client.close()
        spider.logger.info('close spider')

    def process_item(self, item, spider):

        if 'city_urls' in item:
            city_urls = dict(item).get('city_urls')
            for url in city_urls:
                save_city_redis(url)
                spider.logger.info('save_city_redis %s' % url)

        if 'main_category' in item:
            main_category = dict(item).get('main_category')
            for url in main_category:
                save_main_category(url)
                spider.logger.info('save_main_category %s' % url)

        if 'detail_category' in item:
            detail_category = dict(item).get('detail_category')
            for url in detail_category:
                save_detail_category(url)
                spider.logger.info('save_detail_category %s' % url)
        if 'company_urls' in item:
            company_urls = dict(item).get('company_urls')
            for url in company_urls:
                save_company_redis(url)

        if 'business_model' in item:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
            spider.logger.info('save %s to mongo' % item)
            return item
