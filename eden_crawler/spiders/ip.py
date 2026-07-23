import json
import scrapy
from eden_crawler.items import DynamicItem


class IpSpider(scrapy.Spider):
    name = "ip"
    # start_urls = ["http://ip-api.com/json"]

    async def start(self):
        yield scrapy.Request("http://ip-api.com/json", callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        item = DynamicItem()
        item["ip"] = data.get("query")
        item["country"] = data.get("country")
        item["region"] = data.get("regionName")
        item["city"] = data.get("city")
        item["org"] = data.get("org")
        yield item