"""Spider"""
from abc import ABC

import scrapy
from bs4 import BeautifulSoup

from src.config import settings
from src.items import CompanyInfoItem, CrawlEnterpriseInfoItem
from src.storage.redis_storage import category_save_redis, read_redis_list


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


class CityCategorySpider(scrapy.Spider, ABC):
    """
    city Category Spider
    """
    name = 'city_category_spider'
    start_urls = ['https://b2b.11467.com/']

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
            item['urls'] = u.css('a::attr(href)').getall()  # 所有link

        for u in check_city_url(item.get('urls')):
            category_save_redis('category_urls', u)
        return item


class ParseCategoryUrl(scrapy.Spider, ABC):
    """
    为读city category url列表 获取分类链接
    """
    name = 'parse_category_url'
    start_urls = read_redis_list('category_urls')
    headers = settings.get('all_category').get('ua')

    for url in start_urls:

        scrapy.Request(url, headers=headers)

    async def parse(self, response, **kwargs):
        items = []
        item = CrawlEnterpriseInfoItem()
        urls_list = response.xpath('//*[@id="il"]')
        for url in urls_list:
            item['main_category'] = url.css('a::attr(href)').getall()
            items.append(item)

        for u in check_city_url(item.get('main_category')):
            category_save_redis('main_category_urls', u)

        print(items)


class ParseDetailCategory(scrapy.Spider, ABC):
    """
    解析详情分类链接
    """
    name = 'parse_detail_category'
    start_urls = read_redis_list('main_category_urls')
    headers = settings.get('detail_category').get('ua')

    for url in start_urls:
        scrapy.Request(url, headers=headers)

    async def parse(self, response, **kwargs):
        item = CrawlEnterpriseInfoItem()
        urls_list = response.xpath('//*[@id="il"]')
        for url in urls_list:
            info_list = url.css('a::attr(href)').getall()

        for u in check_city_url(item.get('detail_category')):
            category_save_redis('detail_category', u)


class ParseCompanyInfo(scrapy.Spider):
    """
    Parse Company Info
    """
    name = 'parse_company_info'
    allowed_domains = ['parse_company_info.org']

    # headers = settings.get('city_category').get('start_urls')
    # start_urls = settings.get('city_category').get('ua')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.5005.63 Safari/537.36'}
    start_urls = [
        'https://www.11467.com/changsha/co/76030.htm'
    ]
    for url in start_urls:
        scrapy.Request(url, headers=headers)

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, headers=self.headers)

    async def parse(self, response, **kwargs):
        """
        解析公司详情页信息
        :param response:
        :param kwargs:
        :return:
        """
        item = CompanyInfoItem()
        soup = await BeautifulSoup(response.text, 'html.parser')
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
