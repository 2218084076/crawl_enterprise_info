# proxy = settings.get('proxy_list')
# print(proxy)
import logging

from crawl_enterprise_info.config import settings

mongo_url = settings.MONGO_URL
proxy = settings.PROXY_LIST
headers = settings.HEADERS
print(mongo_url)
print(proxy)
print(headers)
logging.warning('AA')