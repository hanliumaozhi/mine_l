# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from baidu.items import BaiduItem
from scrapy.http.request import Request


class tiebaSpider(scrapy.Spider):
    name = "tieba"
    allowed_domains = ["baidu.com"]
    start_urls = ['http://tieba.baidu.com/f?kw=%E6%B1%89%E6%9C%8D%E6%B0%B4%E5%90%A7&ie=utf-8&pn=0']
    pre_url = "http://tieba.baidu.com/f?kw=%E6%B1%89%E6%9C%8D%E6%B0%B4%E5%90%A7&ie=utf-8&pn="
    index_url = 0
    
    def paese_content(self, content):
        name = Selector(text=content).xpath('//div[@class="threadlist_text threadlist_title j_th_tit  "]/a/text()').extract()[0]
        author = Selector(text=content).xpath('//a[@class="j_user_card  "]/text()').extract()[0]
        timex = Selector(text=content).xpath('//span[@class="threadlist_reply_date j_reply_data"]/text()').extract()
        if len(timex) == 0:
            timex = "00-00"
        else:
            timex = timex[0]
        return (name, author, timex)
        
    
    def parse(self, response):
        all_content = response.xpath('//div[@class="threadlist_li_right j_threadlist_li_right"]').extract()
        for one_content in all_content:
            item = BaiduItem()
            content_info = self.paese_content(one_content)
            item['post_name'], item['post_author'], item['last_repy_time'] = content_info[0], content_info[1], content_info[2]
            yield item
        if self.index_url < 100:
            self.index_url += 50
            complete_url = self.pre_url + str(self.index_url)
            yield Request(complete_url)
            
        
            