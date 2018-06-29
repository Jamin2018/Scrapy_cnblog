# -*- coding:utf-8 -*-


import scrapy
from scrapy import Selector
from cnblogSpider.items import CnblogspiderItem

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

class CnblogsSpider(scrapy.Spider):
    name = "cnblogs"  # 爬虫名称
    allowed_domains = ["cnblogs.com"]  # 允许的域名
    start_urls = [
        "https://www.cnblogs.com/qiyeboy/default.html?page=1"
    ]

    def parse(self, response):
        # 实现网络的解析
        # 首先抽取所有的文章
        papers = response.xpath(".//*[@class='day']")
        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]

            title = paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='c_b_p_desc']/text()").extract()[0]
            item = CnblogspiderItem(url = url, title = title, time = time, content = content)
            request = scrapy.Request(url=url,callback=self.parse_body)
            request.meta['item'] = item
            # yield item
            yield request
            # print url,title,time
        next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
        print next_page
        if next_page:
            yield scrapy.Request(url=next_page[0],callback=self.parse)

    def parse_body(self, response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='postBody']")
        item['image_urls'] = body.xpath('.//img//@src').extract()
        yield item
#
# if __name__ == '__main__':
#     configure_logging()
#     runner = CrawlerRunner()
#     runner.crawl(CnblogsSpider)
#     d = runner.join()
#     d.addBoth(lambda _: reactor.stop())
#     reactor.run()
