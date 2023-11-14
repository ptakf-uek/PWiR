import scrapy


class FreeproxylistNetSpider(scrapy.Spider):
    name = "freeproxylist-net"
    allowed_domains = ["free-proxy-list.net"]
    start_urls = ["https://free-proxy-list.net"]

    def parse(self, response):
        for row in response.css("div.table-responsive table.table tbody tr"):
            yield {
                "ip_address": row.css("td:nth-child(1)::text").get(),
                "port": row.css("td:nth-child(2)::text").get(),
                "country": row.css("td:nth-child(4)::text").get()  # 3rd child is country code.
            }
