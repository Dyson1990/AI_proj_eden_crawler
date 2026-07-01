BOT_NAME = "eden_crawler"
SPIDER_MODULES = ["eden_crawler.spiders"]
NEWSPIDER_MODULE = "eden_crawler.spiders"
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    "eden_crawler.middlewares.ProxyMiddleware": 100,
}

ITEM_PIPELINES = {
    "eden_crawler.pipelines.SQLitePipeline": 300,
}

# V2Ray proxy: system proxy typically listens on 127.0.0.1:10809 or 1080
PROXY_ENABLED = True
PROXY_URL = "http://127.0.0.1:10808"

LOG_LEVEL = "INFO"
