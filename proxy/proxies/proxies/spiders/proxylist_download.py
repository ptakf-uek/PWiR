import scrapy


class ProxylistDownloadSpider(scrapy.Spider):
    name = "proxylist_download"
    allowed_domains = ["www.proxy-list.download"]
    start_urls = ["https://www.proxy-list.download/HTTP"]

    def parse(self, response):
        for row in response.css("table#example1 tbody tr"):
            yield {
                "ip_address": row.css("td:nth-child(1)::text").get().strip(),
                "port": row.css("td:nth-child(2)::text").get().strip(),
                "country": row.css("td:nth-child(4) a::text").get().strip()
            }

# There are two APIs available, although neither of them allows bots to simply scrape them:
# https://www.proxy-list.download/api/v1/get?type=http&country=US
# https://www.proxy-list.download/api/v2/get?l=en&t=http
