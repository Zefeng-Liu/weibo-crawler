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
            
           
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "http://quotes.toscrape.com/page/1",
        "http://quotes.toscrape.com/page/2"
    ]
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_frist(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
            
        next_page_url = response.css('li.next a::attr(href)').extract_first()
        if next_page_url is not None:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)
