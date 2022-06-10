import asyncio
import hashlib
import logging
import random
import time

import aiohttp
import redis
import requests
from bs4 import BeautifulSoup

from crawl_enterprise_info.config import settings
from crawl_enterprise_info.storage.redis_storage import save_redis

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s - %(funcName)s - %(lineno)d: ')


# start_urls = ['//b2b.11467.com/search/1.htm', '//b2b.11467.com/search/35.htm', '//b2b.11467.com/search/62.htm',
#               '//b2b.11467.com/search/549.htm', '//b2b.11467.com/search/563.htm', '//b2b.11467.com/search/578.htm',
#               '//b2b.11467.com/search/625.htm', '//b2b.11467.com/search/645.htm', '//b2b.11467.com/search/748.htm',
#               '//b2b.11467.com/search/757.htm', '//b2b.11467.com/search/774.htm', '//b2b.11467.com/search/779.htm',
#               '//b2b.11467.com/search/813.htm', '//b2b.11467.com/search/836.htm', '//b2b.11467.com/search/860.htm',
#               '//b2b.11467.com/search/877.htm', '//b2b.11467.com/search/893.htm', '//b2b.11467.com/search/914.htm',
#               '//b2b.11467.com/search/3338.htm', '//b2b.11467.com/search/3339.htm',
#               '//b2b.11467.com/search/3340.htm',
#               '//b2b.11467.com/search/3341.htm', '//b2b.11467.com/search/3342.htm',
#               '//b2b.11467.com/search/3343.htm',
#               '//b2b.11467.com/search/3344.htm', '//b2b.11467.com/search/3345.htm',
#               '//b2b.11467.com/search/3346.htm',
#               '//b2b.11467.com/search/3347.htm', '//b2b.11467.com/search/3348.htm',
#               '//b2b.11467.com/search/3349.htm',
#               '//b2b.11467.com/search/3350.htm', '//b2b.11467.com/search/3351.htm',
#               '//b2b.11467.com/search/3352.htm',
#               '//b2b.11467.com/search/3353.htm', '//b2b.11467.com/search/3354.htm',
#               '//b2b.11467.com/search/3355.htm',
#               '//b2b.11467.com/search/3356.htm', '//b2b.11467.com/search/3357.htm',
#               '//b2b.11467.com/search/3358.htm',
#               '//b2b.11467.com/search/3359.htm', '//b2b.11467.com/search/3360.htm',
#               '//b2b.11467.com/search/3361.htm',
#               '//b2b.11467.com/search/3362.htm', '//b2b.11467.com/search/3363.htm',
#               '//b2b.11467.com/search/3364.htm',
#               '//b2b.11467.com/search/3365.htm', '//b2b.11467.com/search/3366.htm',
#               '//b2b.11467.com/search/3367.htm',
#               '//b2b.11467.com/search/3368.htm', '//b2b.11467.com/search/3369.htm',
#               '//b2b.11467.com/search/3371.htm',
#               '//b2b.11467.com/search/3372.htm', '//b2b.11467.com/search/3374.htm',
#               '//b2b.11467.com/search/11739.htm',
#               '//b2b.11467.com/search/12104.htm', '//b2b.11467.com/search/11986.htm',
#               '//b2b.11467.com/search/11994.htm',
#               '//b2b.11467.com/search/12123.htm', '//b2b.11467.com/search/11741.htm',
#               '//b2b.11467.com/search/11922.htm',
#               '//b2b.11467.com/search/4167.htm', '//b2b.11467.com/search/12020.htm',
#               '//b2b.11467.com/search/12112.htm',
#               '//b2b.11467.com/search/10281.htm', '//b2b.11467.com/search/5781.htm',
#               '//b2b.11467.com/search/12025.htm',
#               '//b2b.11467.com/search/11989.htm', '//b2b.11467.com/search/10309.htm',
#               '//b2b.11467.com/search/12075.htm',
#               '//b2b.11467.com/search/11750.htm', '//b2b.11467.com/search/1.htm', '//b2b.11467.com/search/2.htm',
#               '//b2b.11467.com/search/3.htm', '//b2b.11467.com/search/4.htm', '//b2b.11467.com/search/5.htm',
#               '//b2b.11467.com/search/6.htm', '//b2b.11467.com/search/7.htm', '//b2b.11467.com/search/8.htm',
#               '//b2b.11467.com/search/9.htm', '//b2b.11467.com/search/10.htm', '//b2b.11467.com/search/11.htm',
#               '//b2b.11467.com/search/12.htm', '//b2b.11467.com/search/13.htm', '//b2b.11467.com/search/14.htm',
#               '//b2b.11467.com/search/15.htm', '//b2b.11467.com/search/-60ac6d6e7269548c.htm',
#               '//b2b.11467.com/search/-6d8896326a2162df8bad7ec356686750.htm',
#               '//b2b.11467.com/search/-91526c34751f4ea77ebf.htm',
#               '//b2b.11467.com/search/-90536613901a.htm', '//b2b.11467.com/search/-6c7d6ce1888b819c.htm',
#               '//b2b.11467.com/search/-6c348f6c53706c348d34.htm',
#               '//b2b.11467.com/search/-5de54e1a4e9280547f515b9e8bad.htm',
#               '//b2b.11467.com/search/-516c4f1a51659a7b.htm', '//b2b.11467.com/search/-5b9e8bad5ba45e7353f0.htm']


def get_md5(val):
    """
    把目标数据进行哈希，用哈希值去重更快
    :param val:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(val.encode('utf-8'))
    return md5.hexdigest()


def add_url(url) -> bool:
    """
    添加redis验证是否唯一
    :param url:
    :return:
    """
    red = redis.Redis(host='localhost', port=6379, db=0)
    res = red.sadd(settings.URLSET, get_md5(url))  # 注意是 保存set的方式
    if res == 0:  # 若返回0,说明插入不成功，表示有重复
        return False
    else:
        return True


async def crawl_city_category():
    """
    抓取所有城市分类连接
    :return:
    """
    city_category_list = []
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://b2b.11467.com/',
                                   headers=settings.HEADERS) as response:
                logging.debug('get %s ' % response)
                soup = BeautifulSoup(await response.text(), 'html.parser')
                box_list = soup.find_all('a')
                for d in box_list:
                    url = d.get('href')
                    if 'www' in url and 'http' not in url:
                        url = 'http:' + url
                        if len(list(url)) > 19:
                            city_category_list.append(url)
                logging.debug(city_category_list)
                return city_category_list
        except Exception as e:
            logging.debug('Error %s' % e)


async def crawl_main_category_url(city_list: list):
    """
    crawl main category url
    抓取city下面主要分类链接
    :param city_list:
    :return:
    """
    for u in city_list:
        time.sleep(random.randint(3, 8))
        async with aiohttp.ClientSession() as session:
            async with session.get(u, headers=settings.HEADERS) as response:
                logging.debug('Get <%s>' % u)
                soup = BeautifulSoup(await response.text(), 'html.parser')
                box_list = soup.find_all('a')
                for i in box_list:
                    url = i['href']
                    if add_url(url):
                        if 'https://www.11467.com/' in url:
                            save_redis(settings.get('main_category_name'), url)
                            # logging.debug('<%s> save %s' % (url, settings.get('main_category_name')))
                    else:
                        logging.debug('已存在')


async def crawl_detailed_category(main_category: list):
    """
    crawl crawl category
    抓取主分类下所有详细分类链接
    :param main_category:
    :return:
    """
    for u in main_category:
        if 'http' not in u:
            u = 'https' + u
            logging.debug(u)
            time.sleep(random.randint(5, 10))
            async with aiohttp.ClientSession() as session:
                async with session.get(u, headers=settings.HEADERS) as response:
                    logging.debug('Get %s' % response)
                    await asyncio.sleep(random.randint(3, 8))
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    box_list = soup.find_all('a')
                    for i in box_list:
                        url = i['href']
                        if 'search/' in url:
                            save_redis(settings.get('detailed_category_name'), url)
                            # logging.debug('<%s> save %s' % (url, settings.get('detailed_category_name')))
                        if 'https://www.11467.com/' in url and '.htm' in url:
                            save_redis(settings.get('detailed_category_name'), url)
                            # logging.debug('<%s> save %s' % (url, settings.get('detailed_category_name')))
                        if '//www.11467.com/' in url and 'http' not in url and url != '//www.11467.com/':
                            url = 'https:' + url
                            save_redis(settings.get('company_redis_name'), url)
                            logging.debug('<%s> save redis %s' % (url, settings.get('company_redis_name')))


async def crawl_company_link(url: str):
    """
    crawl company link
    通过上面详细分类页面抓取所有公司详情页链接
    :param url:
    :return:
    """
    if add_url(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=settings.HEADERS) as response:
                await asyncio.sleep(random.randint(5, 10))
                soup = BeautifulSoup(await response.text(), 'html.parser')
                box_list = soup.find_all('a')
                for i in box_list:
                    url = i['href']
                    if '//www.11467.com/' in url and 'http' not in url and url != '//www.11467.com/':
                        url = 'https:' + url
                        save_redis(settings.get('company_redis_name'), url)
                        # logging.debug('<%s> save redis %s' % (url, settings.get('company_redis_name')))
    else:
        logging.debug('已存在')


def parse_company_info(url: str) -> dict:
    """
    parse company info
    解析公司详情页工商信息
    :param url:
    :return:
    """
    if add_url(url):
        response = requests.get(url,
                                headers=settings.HEADERS,
                                proxies=random.choice(settings.PROXY_LIST)
                                )
        logging.debug('response.status_code %s ' % response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            info_box = soup.find_all('td')
            info_list = []
            for i in info_box:
                info_list.append(i.get_text())

            key_list = info_list[::2]
            value_list = info_list[1::2]
            result_json = dict(zip(key_list, value_list))
            info_json = {
                "company_name": result_json.get('法人名称：', ''),
                "product": result_json.get('主要经营产品：', ''),
                "business_scope": result_json.get('经营范围：', ''),
                "license_num": result_json.get('营业执照：', ''),
                "business_status": result_json.get('经营状态：', ''),
                "business_model": result_json.get('经营模式：', ''),
                "capital": result_json.get('注册资本：', ''),
                "category": result_json.get('所属分类：', ''),
                "city": result_json.get('所属城市：', ''),
                "company_code": result_json.get('顺企编码：', ''),
                "shop_link": result_json.get('商铺：', '')
            }
            logging.debug('parse <%s> info is %s' % (url, info_json))
            return info_json
        else:
            save_redis(settings.get('rollback'), url)
    else:
        logging.debug('已存在')
