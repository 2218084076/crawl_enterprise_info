"""runer"""
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from spiders.spider import CityCategorySpider, ParseMainCategory, ParseDetailCategory, ParseCompanyInfo, \
    ParseCompanyLink

configure_logging()
settings = get_project_settings()

runner = CrawlerRunner(settings)
runner.crawl(CityCategorySpider)
# runner.crawl(ParseMainCategory)
# runner.crawl(ParseDetailCategory)
# runner.crawl(ParseCompanyLink)
# runner.crawl(ParseCompanyInfo)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
