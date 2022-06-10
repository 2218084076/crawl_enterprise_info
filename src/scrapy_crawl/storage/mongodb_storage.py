"""company infos DB"""
import logging

import pymongo

logger = logging.getLogger(__name__)


def init_mongo(company_info: dict):
    """
    init mongoDB
    :param company_info:
    """
    client = pymongo.MongoClient('localhost:27017')

    save_to_mongo(company_info, client)


def save_to_mongo(company_info: dict, my_client):
    """
    company info save to mongo
    :param company_info:
    :param my_client:
    """
    mydb = my_client['company_info']
    print(mydb.list_collection_names())
    x = mydb['company info'].insert_one(company_info)  # 增
    logger.debug('save %s' % company_info)
