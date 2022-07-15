# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random

import settings
from faker import Faker
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)


class CrawlBusinessInfoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        """
        from_crawler
        :param crawler:
        :return:
        """
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        """
        process_spider_input
        :param spider:
        :return:
        """
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        """
        process_spider_output
        :param response:
        :param result:
        :param spider:
        :return:
        """
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        spider.logger.info('CrawlBusinessInfoSpiderMiddleware spider', spider)
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """
        process_spider_exception
        :param response:
        :param exception:
        :param spider:
        :return:
        """
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        """
        process_start_requests
        :param start_requests:
        :param spider:
        :return:
        """
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        """
        spider_opened
        :param spider:
        :return:
        """
        spider.logger.info('Spider opened: %s' % spider.name)

    def process_request(self, request, spider):
        """
        process_request
        :param request:
        :param spider:
        :return:
        """
        f = Faker()
        agent = f.firefox()
        request.headers['User-Agent'] = agent


class CrawlBusinessInfoDownloaderMiddleware:
    """Crawl Business Info Downloader Middleware"""

    @classmethod
    def from_crawler(cls, crawler):
        """
        from_crawler
        :param crawler:
        :return:
        """

        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        process_request
        :param request:
        :param spider:
        :return:
        """
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        """
        process_exception
        :param request:
        :param exception:
        :param spider:
        :return:
        """
        pass

    def spider_opened(self, spider):
        """
        spider_opened
        :param spider:
        :return:
        """
        spider.logger.info('Spider opened: %s' % spider.name)


class CrawlBusinessInfoProxyMiddleware:
    """Proxy Middleware"""

    def process_request(self, request, spider):
        """
        process_request
        :param request:
        :param spider:
        :return:
        """
        proxy = random.choice(settings.get('MY_PROXY'))
        if proxy:
            request.meta['proxy'] = proxy
            yield request


class CrawlBusinessInfoRetryMiddleware(RetryMiddleware):
    """
    Retry Middleware
    重试
    """

    def process_response(self, request, response, spider):
        """
        process_response
        :param request:
        :param response:
        :param spider:
        :return:
        """
        if request.meta.get('dont_retry', False):
            logger.info('response', response)
            return response

        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            logger.info('reason', reason)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        """
        process_exception
        :param request:
        :param exception:
        :param spider:
        :return:
        """
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and request.meta.get('dont_retry', False):
            logger.info('process_exception')
            return self._retry(request, exception, spider)
