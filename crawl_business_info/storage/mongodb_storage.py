"""company infos DB"""
import logging

import pymongo

logging.basicConfig(filename='example.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s - %(funcName)s - %(lineno)d: ',
                    )


class CompanyInfoMongo:

    def __init__(self):
        self.mydb = None
        self.my_col = None
        self.db_name = 'company_info'
        self.collection_name = 'company_info'
        self.my_client = pymongo.MongoClient('localhost:27017')

    def save_company_info(self, company_info: dict):
        """
        save company info
        :param company_info:
        :return:
        """
        mydb = self.my_client[self.db_name]
        my_col = mydb[self.collection_name]
        my_col.insert_one(company_info)
        logging.debug('Save company info <%s> to mongoDB' % company_info)
