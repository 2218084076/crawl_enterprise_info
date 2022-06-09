"""company infos DB"""
import logging

import pymongo

from crawl_enterprise_info.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s - %(funcName)s')


def init_mongo(company_info):
    """
    init mongoDB
    :param company_info:
    """
    mongo_url = settings.MONGO_URL
    client = pymongo.MongoClient(mongo_url)

    save_to_mongo(company_info, client)


def save_to_mongo(company_info: dict, my_client):
    """
    company info save to mongo
    :param company_info:
    :param my_client:
    """
    mydb = my_client['company_info']
    mydb['company_info'].insert_one(company_info)  # 增
    logger.debug('save %s' % company_info)
