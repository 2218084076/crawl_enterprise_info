"""runer"""
import logging

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

from spiders.spider import ParseCompanyLink, ParseCompanyInfo, CityCategorySpider, ParseMainCategory, \
    ParseDetailCategory

logger = logging.getLogger(__name__)

configure_logging()
settings = get_project_settings()

runner = CrawlerRunner(settings)

runner.crawl(CityCategorySpider)
runner.crawl(ParseMainCategory)
runner.crawl(ParseDetailCategory)
runner.crawl(ParseCompanyLink)
runner.crawl(ParseCompanyInfo)

d = runner.join()
d.addBoth(lambda _:reactor.stop())

reactor.run()
