"""Spider"""
import logging

import scrapy
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings

from crawl_business_info.items import CompanyInfoItem, CrawlEnterpriseInfoItem
from crawl_business_info.storage.redis_storage import read_redis

settings = get_project_settings()


def check_city_url(items: list):
    """
    check url
    :param items:
    :return:
    """
    urls = []

    for i in items:
        if '//www.11467.com' in i:
            if 'http' not in i:
                url = 'http:%s' % i
                urls.append(url)

    return urls


class CityCategorySpider(scrapy.Spider):
    """
    city Category Spider
    """
    name = 'city_category_spider'
    start_urls = ['https://b2b.11467.co']

    def parse(self, response, **kwargs):
        """
        解析分类链接
        :param response:
        :param kwargs:
        :return:
        """
        item = CrawlEnterpriseInfoItem()
        urls_list = response.xpath('//*[@id="il"]')
        for u in urls_list:
            item['city_urls'] = u.css('a::attr(href)').getall()  # 所有城市link

        return item


class ParseMainCategory(scrapy.Spider):
    """
    为读city category url列表 获取分类链接
    """
    name = 'parse_main_category'
    start_urls = read_redis('city')

    def parse(self, response, **kwargs):
        item = CrawlEnterpriseInfoItem()
        urls_list = response.xpath('//*[@id="il"]')
        for url in urls_list:
            item['main_category'] = url.css('a::attr(href)').getall()

        return item


class ParseDetailCategory(scrapy.Spider):
    """
    解析详情分类链接
    """
    name = 'parse_detail_category'
    start_urls = read_redis('main_category')

    def parse(self, response, **kwargs):
        item = CrawlEnterpriseInfoItem()
        urls_list = response.xpath('//*[@id="il"]')
        for url in urls_list:
            item['detail_category'] = url.css('a::attr(href)').getall()

        return item


class ParseCompanyLink(scrapy.Spider):
    """
    解析公司详情页
    """
    name = 'parse_company_link'
    start_urls = read_redis('detail_category')

    def parse(self, response, **kwargs):
        item = CrawlEnterpriseInfoItem()
        tag_list = response.xpath('//*[@id="il"]')
        for t in tag_list:
            item['company_urls'] = t.css('a::attr(href)').getall()

        return item


class ParseCompanyInfo(scrapy.Spider):
    """
    Parse Company Info
    """
    name = 'parse_company_info'
    allowed_domains = ['parse_company_info.org']
    start_urls = read_redis('company_links')

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

        return item
