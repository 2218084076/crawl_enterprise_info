# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlEnterpriseInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    urls = scrapy.Field()
    main_category=scrapy.Field()
    detail_category = scrapy.Field()
    pass


class CompanyInfoItem(scrapy.Item):
    """Company Info Item"""
    company_name = scrapy.Field()
    product = scrapy.Field()  # 主要经营产品
    business_scope = scrapy.Field()  # 经营范围
    license_num = scrapy.Field()  # 营业执照
    business_status = scrapy.Field() # 经营状态
    business_model = scrapy.Field() # 经营模式
    capital = scrapy.Field() # 注册资本
    category = scrapy.Field()
    city = scrapy.Field()
    company_code = scrapy.Field()
    shop_link = scrapy.Field()
    pass
