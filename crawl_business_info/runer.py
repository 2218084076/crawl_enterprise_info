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


@defer.inlineCallbacks
def crawl():
    # yield runner.crawl(CityCategorySpider)
    yield runner.crawl(ParseMainCategory)
    yield runner.crawl(ParseDetailCategory)
    # yield runner.crawl(ParseCompanyLink)
    # yield runner.crawl(ParseCompanyInfo)
    reactor.stop()


crawl()
reactor.run()
