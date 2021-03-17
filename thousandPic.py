import scrapy


class ThousandpicSpider(scrapy.Spider):
    name = 'thousandPic'
    allowed_domains = ['www.58pic.com']
    start_urls = ['http://www.58pic.com/']

    def parse(self, response):
        pass
