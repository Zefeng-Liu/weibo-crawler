from scrapy import cmdline
import os

if not os.path.exists('testlog'):
    os.mkdir('testlog')

cmdline.execute("scrapy crawl sinaSpider".split())
