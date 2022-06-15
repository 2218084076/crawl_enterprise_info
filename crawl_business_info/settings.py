# Scrapy settings for crawl_business_info project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

MY_PROXY = ['http://61.144.152.209:9000', 'http://218.67.94.23:5555', 'http://114.249.112.121:9000',
            'http://222.69.240.130:8001', 'http://218.1.200.156:57114', 'http://218.86.87.171:31661',
            'http://123.56.175.31:3128', 'http://120.220.220.95:8085', 'http://111.225.153.123:8089',
            'http://122.226.57.70:8888', 'http://61.191.56.60:8085', 'http://47.100.255.35:80',
            'http://47.92.113.71:80', 'http://223.96.90.216:8085', 'http://218.1.200.167:57114',
            'http://120.194.55.139:6969', 'http://112.6.117.135:8085', 'http://111.225.153.100:8089',
            'http://112.6.117.178:8085', 'http://1.15.226.140:3128', 'http://221.217.50.129:9000',
            'http://112.65.86.247:8118', 'http://47.113.90.161:83', 'http://47.112.122.163:82',
            'http://27.157.230.138:7082', 'http://123.163.55.123:3128', 'http://111.225.153.145:8089',
            'http://124.226.138.114:9797', 'http://47.111.176.17:88']

BOT_NAME = 'crawl_business_info'

SPIDER_MODULES = ['crawl_business_info.spiders']
NEWSPIDER_MODULE = 'crawl_business_info.spiders'

# retry settibgs
RETRY_PROXY=True
RETRY_TIMES = 3


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'crawl_business_info (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'crawl_business_info.middlewares.CrawlBusinessInfoSpiderMiddleware': 543,

}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'crawl_business_info.middlewares.CrawlBusinessInfoDownloaderMiddleware': 543,
    'crawl_business_info.middlewares.CrawlBusinessInfoProxyMiddleware': 543,
    'crawl_business_info.middlewares.CrawlBusinessInfoRetryMiddleware':543
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'crawl_business_info.pipelines.CrawlBusinessInfoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
