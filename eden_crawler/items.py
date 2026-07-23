import scrapy


class Asset:
    """Mark a URL for download. type: 'file' → local path, 'blob' → binary in DB."""
    def __init__(self, url, type="blob"):
        self.url = url
        self.type = type


class DynamicItem(scrapy.Item):
    """Auto-register fields on first assignment — no need to pre-define them."""

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super().__setitem__(key, value)
