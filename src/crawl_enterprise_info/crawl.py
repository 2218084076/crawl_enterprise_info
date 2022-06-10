import asyncio
import hashlib
import logging
import random
import time

import aiohttp
import redis
from bs4 import BeautifulSoup

from crawl_enterprise_info.config import settings
from crawl_enterprise_info.storage.redis_storage import save_redis

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s - %(funcName)s - %(lineno)d: ',
                    # filename='logfile.log',
                    # filemode='w'
                    )
logger = logging.getLogger()


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


async def crawl_city_category(url):
    """
    抓取所有城市分类连接
    :return:
    """
    city_category_list = []
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url,
                                   headers=settings.HEADERS) as response:
                logger.debug('get %s ' % response)
                await asyncio.sleep(random.randint(5, 10))
                soup = BeautifulSoup(await response.text(), 'html.parser')
                box_list = soup.find_all('a')
                for d in box_list:
                    url = d.get('href')
                    if 'www' in url and 'http' not in url:
                        url = 'http:' + url
                        if len(list(url)) > 19:
                            city_category_list.append(url)
                logger.debug(city_category_list)
                return city_category_list
        except Exception as e:
            logger.debug('Error %s' % e)


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
                logger.debug('Get <%s>' % u)
                await asyncio.sleep(random.randint(5, 10))
                soup = BeautifulSoup(await response.text(), 'html.parser')
                box_list = soup.find_all('a')
                for i in box_list:
                    url = i['href']
                    if add_url(url):
                        if 'https://www.11467.com/' in url:
                            save_redis(settings.get('main_category_name'), url)
                            # logging.debug('<%s> save %s' % (url, settings.get('main_category_name')))
                    else:
                        logger.debug('已存在')


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
            logger.debug(u)
            time.sleep(random.randint(5, 10))
            async with aiohttp.ClientSession() as session:
                async with session.get(u, headers=settings.HEADERS) as response:
                    logger.debug('Get %s' % response)
                    await asyncio.sleep(random.randint(5, 10))
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    box_list = soup.find_all('a')
                    for i in box_list:
                        url = i['href']
                        if 'search/' in url:
                            save_redis(settings.get('detailed_category_name'), url)
                            # logger.debug('<%s> save %s' % (url, settings.get('detailed_category_name')))
                        if 'https://www.11467.com/' in url and '.htm' in url:
                            save_redis(settings.get('detailed_category_name'), url)
                            # logger.debug('<%s> save %s' % (url, settings.get('detailed_category_name')))
                        if '//www.11467.com/' in url and 'http' not in url and url != '//www.11467.com/':
                            url = 'https:' + url
                            save_redis(settings.get('company_redis_name'), url)
                            logger.debug('<%s> save redis %s' % (url, settings.get('company_redis_name')))


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
                        # logger.debug('<%s> save redis %s' % (url, settings.get('company_redis_name')))
    else:
        logger.debug('已存在')


async def parse_company_info(url: str) -> dict:
    """
    parse company info
    解析公司详情页工商信息
    :param url:
    :return:
    """
    if add_url(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   headers=settings.HEADERS,
                                   ) as response:
                logger.debug('response.status_code %s ' % response.status)
                await asyncio.sleep(random.randint(5, 10))
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
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
                    logger.debug('parse <%s> info is %s' % (url, info_json))
                    return info_json
                else:
                    save_redis(settings.get('rollback'), url)
    else:
        logger.debug('已存在')
