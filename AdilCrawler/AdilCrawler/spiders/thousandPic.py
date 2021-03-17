# -*- coding: utf-8 -*-
import scrapy
# 这里使用 import 或是 下面from 的方式都行，关键要看 当前项目在pycharm的打开方式，是否是作为一个项目打开的，建议使用这一种方式。
import AdilCrawler.items as items

# 使用from 这种方式，AdilCrawler 需要作为一个项目打开。
# from AdilCrawler.items import AdilcrawlerItem


class ThousandpicSpider(scrapy.Spider):
    name = 'thousandPic'
    allowed_domains = ['www.58pic.com']
    start_urls = ['http://www.58pic.com/c/']

    def parse(self, response):

        '''
        查看页面元素
         /html/body/div[4]/div[3]/div/a/p[2]/span/span[2]/text()
          因为页面中 有多张图，而图是以 /html/body/div[4]/div[3]/div[i]  其中i  为变量 作为区分的 ，所以为了获取当前页面所有的图
          这里 不写 i 程序会遍历 该 路径下的所有 图片。
        '''

        item = items.AdilcrawlerItem()

        # author 作者
        # theme  主题

        author = response.xpath('/html/body/div[4]/div[3]/div/a/p[2]/span/span[2]/text()').extract()

        theme = response.xpath('/html/body/div[4]/div[3]/div/a/p[1]/span[1]/text()').extract()

        item['author'] = author
        item['theme']  = theme

        return item