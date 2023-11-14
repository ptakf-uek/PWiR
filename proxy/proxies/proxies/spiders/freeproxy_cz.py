import scrapy
import base64


class FreeproxyCzSpider(scrapy.Spider):
    name = "freeproxy-cz"
    allowed_domains = ["free-proxy.cz"]
    start_urls = ["http://free-proxy.cz/en/proxylist/country/all/https/ping/all"]

    def parse(self, response):
        for row in response.css("table#proxy_list tbody tr"):
            yield {
                "ip_address": self.getIpAddress(row.css("td:nth-child(1) script::text").get()),
                "port": row.css("td:nth-child(2) span.fport::text").get(),
                "country": row.css("td:nth-child(4) a::text").get()
            }

    def getIpAddress(self, js_command):
        return base64.b64decode(js_command[28:-2]).decode()  # Check how many characters actually needs to be removed.
