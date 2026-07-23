import scrapy


class DynamicItem(scrapy.Item):
    """Auto-register fields on first assignment — no need to pre-define them."""

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super().__setitem__(key, value)
