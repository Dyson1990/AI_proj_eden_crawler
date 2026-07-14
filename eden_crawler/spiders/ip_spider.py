import json
import scrapy
# from eden_crawler.items import IpCheckItem


class IpSpider(scrapy.Spider):
    name = "ip"
    start_urls = ["http://ip-api.com/json"]

    def parse(self, response):
        data = json.loads(response.text)
        print(f"#################################### IP:{data.get("country")}【{data.get("query")}】 ####################################")
        # yield IpCheckItem(
        #     ip=data.get("query"),
        #     country=data.get("country"),
        #     region=data.get("regionName"),
        #     city=data.get("city"),
        #     org=data.get("org"),
        # )
