__author__ = 'rich'


from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from WhiteHouse.items import WhitehouseItem


class MySpider(Spider):
    name = "whitehouse"
    allowed_domains = ["whitehouse.gov"]
    start_urls = ["http://www.whitehouse.gov/engage/latest-news"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//li[@views-row]")
        items = []
        print "*******"
        print titles
        print "*******"
        for titles in titles:
            item = WhitehouseItem()
            item["text"] = titles.select("a/text()").extract()
            item["link"] = titles.select("a/@href").extract()
            items.append(item)
        return items
