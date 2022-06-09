"""Test crawl"""
from crawl_enterprise_info.crawl import get_md5


def test_get_md5():
    """test get md5"""
    # test 的哈希值为 098f6bcd4621d373cade4e832627b4f6
    md5 = get_md5('test')
    assert md5 == '098f6bcd4621d373cade4e832627b4f6'


def test_add_url():
    """test add url"""
