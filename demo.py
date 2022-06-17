import re
from crawl_business_info import settings
a = '//www.11467.com/shanghai/co/1007492.htm'
ret = re.match("^//www.11467.com", a)
print(ret)
print(settings.MY_PROXY)
