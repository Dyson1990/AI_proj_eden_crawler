class ProxyMiddleware:
    def process_request(self, request, spider):
        if spider.settings.getbool("PROXY_ENABLED"):
            request.meta["proxy"] = spider.settings.get("PROXY_URL")
