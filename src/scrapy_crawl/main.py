from src.spiders.spider import CityCategorySpider
from src.storage.redis_storage import city_category_save_redis

city_category_spider = CityCategorySpider()



city_category_save_redis()
