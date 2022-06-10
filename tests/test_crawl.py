"""Test crawl"""
from pathlib import Path

import pytest
import redis

from crawl_enterprise_info.crawl import add_url, get_md5


@pytest.fixture(name='test_data_path')
def fixture_test_data_path() -> Path:
    """fixture test data path"""
    return Path(__file__).parent / 'data'


def test_get_md5():
    """test get md5"""
    # test 的哈希值为 098f6bcd4621d373cade4e832627b4f6
    md5 = get_md5('test')
    assert md5 == '098f6bcd4621d373cade4e832627b4f6'


@pytest.mark.parametrize(
    'url',
    [
        'test',
        'foo'
    ]
)
def test_add_url(url):
    """test add url"""

    def del_redis():
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.delete('TEST:urlset')

    del_redis()
    add_url('test')
    if url == 'test':
        assert not add_url(url)
    if url == 'foo':
        assert add_url(url)


@pytest.mark.asyncio
async def test_crawl_city_category(mocker):
    """Test crawl city category"""
