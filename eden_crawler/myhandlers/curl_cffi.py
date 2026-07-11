from curl_cffi import requests
from scrapy.http import HtmlResponse
from twisted.internet import threads


class CurlCffiDownloadHandler:
    def __init__(self, settings):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def download_request(self, request, spider):
        return threads.deferToThread(self._fetch, request)

    def _fetch(self, request):
        proxy = request.meta.get("proxy")
        headers = {k.decode(): v[0].decode() for k, v in request.headers.items()}
        resp = requests.request(
            method=request.method,
            url=request.url,
            headers=headers,
            data=request.body,
            proxy=proxy,
            impersonate="chrome110",
        )
        return HtmlResponse(
            url=resp.url,
            status=resp.status_code,
            headers=resp.headers,
            body=resp.content,
            request=request,
            encoding=resp.encoding or "utf-8",
        )

    def close(self):
        pass
