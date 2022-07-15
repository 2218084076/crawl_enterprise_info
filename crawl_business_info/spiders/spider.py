"""Spider"""
import logging

import scrapy
from bs4 import BeautifulSoup
from crawl_business_info.storage.redis_storage import RedisBase

from crawl_business_info.items import CompanyInfoItem, CrawlEnterpriseInfoItem

logger = logging.getLogger(__name__)


class CityCategorySpider(scrapy.Spider):
    """
    city Category Spider
    """
    name = 'city_category_spider'
    start_urls = ['https://b2b.11467.com']

    def parse(self, response, **kwargs):
        """
        解析分类链接
        :param response:
        :param kwargs:
        :return:
        """
        item = CrawlEnterpriseInfoItem()
        urls_list = response.xpath('//*[@id="il"]')
        for url in urls_list:
            item['city_urls'] = url.css('a::attr(href)').getall()  # 所有城市link

        return item


class ParseMainCategory(scrapy.Spider):
    """
    为读city category url列表 获取分类链接
    """
    redis_base = RedisBase()

    name = 'parse_main_category'
    start_urls = redis_base.read_redis('city')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        items = []
        item = CrawlEnterpriseInfoItem()
        urls_list = response.xpath('//*[@id="il"]')
        for url in urls_list:
            items.extend(url.css('a::attr(href)').getall())
        item['main_category'] = items

        return item


class ParseDetailCategory(scrapy.Spider):
    """
    解析详情分类链接
    """
    redis_base = RedisBase()

    name = 'parse_detail_category'
    start_urls = redis_base.read_redis('main_category')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        items = []
        item = CrawlEnterpriseInfoItem()
        urls_list = response.xpath('//*[@id="il"]')
        for url in urls_list:
            items.extend(url.css('a::attr(href)').getall())
        item['detail_category'] = items

        return item


class ParseCompanyLink(scrapy.Spider):
    """
    解析公司详情页
    """
    redis_base = RedisBase()

    name = 'parse_company_link'
    start_urls = redis_base.read_redis('detail_category')

    def parse(self, response, **kwargs):
        """
        parse
        :param response:
        :param kwargs:
        :return:
        """
        items = []
        item = CrawlEnterpriseInfoItem()
        tag_list = response.xpath('//h4')
        for tag in tag_list:
            items.append(tag.css('a::attr(href)').get())
        item['company_urls'] = items
        return item


class ParseCompanyInfo(scrapy.Spider):
    """
    Parse Company Info
    """
    redis_base = RedisBase()

    name = 'parse_company_info'
    allowed_domains = ['parse_company_info.org']
    start_urls = redis_base.read_redis('company_links')

    def parse(self, response, **kwargs):
        """
        解析公司详情页信息
        :param response:
        :param kwargs:
        :return:
        """
        item = CompanyInfoItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        info_box = soup.find_all('td')
        info_list = []
        for i in info_box:
            info_list.append(i.get_text().split('：')[0])
        key_list = info_list[::2]
        value_list = info_list[1::2]
        result_json = dict(zip(key_list, value_list))
        item['company_name'] = result_json.get('法人名称', '')
        item['product'] = result_json.get('主要经营产品', '')
        item['business_scope'] = result_json.get('经营范围', '')
        item['license_num'] = result_json.get('营业执照', '')
        item['business_status'] = result_json.get('经营状态', '')
        item['business_model'] = result_json.get('经营模式', '')
        item['capital'] = result_json.get('注册资本', '')
        item['category'] = result_json.get('所属分类', '')
        item['city'] = result_json.get('所属城市', '')
        item['company_code'] = result_json.get('顺企编码', '')
        item['shop_link'] = result_json.get('商铺', '')
        logger.info('Spiders.ParseCompanyInfo {}'.format(item))
        return item
