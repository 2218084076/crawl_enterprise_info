import asyncio

from scrapy.crawler import CrawlerProcess

from spiders.spider import CityCategorySpider,ParseCompanyInfo,ParseCategoryUrl

process = CrawlerProcess()
process.crawl(ParseCompanyInfo)
process.start()



