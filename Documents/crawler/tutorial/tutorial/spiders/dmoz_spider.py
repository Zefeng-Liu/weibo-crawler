import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoztools.net"]
    start_urls = [
            "http://dmoztools.net/Computer/Programming/Languages/Python/Books/",
            "http://dmoztools.net/Computer/Programming/Languages/Python/Resouces/"]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
