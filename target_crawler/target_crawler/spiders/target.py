# -*- coding: utf-8 -*-
import scrapy


class TargetSpider(scrapy.Spider):
    name = 'target'
    allowed_domains = ['target.com']

    def __init__(self, url=None, *args, **kwargs):
        super(TargetSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url,]

    def parse(self, response):
        item = {}

        item['url'] = response.url 
        item['tcin'] = response.xpath('//div[b/text()="TCIN"]/text()').extract()[-1]
        item['upc'] = response.xpath('//div[b/text()="UPC"]/text()').extract()[-1]
        item['price'] = response.xpath('//div[@data-test="product-price"]/text()').extract_first()
        item['currency'] = response.xpath('//div[@data-test="product-price"]/text()').extract_first()
        item['title'] = response.xpath('//h1[@itemprop="name"]/span/text()').extract_first()
        item['description'] = response.xpath('//h3[text()="Description"]/following-sibling::div/text()').extract_first()
        item['specs'] = response.xpath('//h3[text()="Specifications"]/following-sibling::div/div/text()').extract_first() 
        item['ingredients'] = response.xpath('//script/text()').re('"ingredients":"[\w\ \,\-\)\(\:\.\/\\\]+')[0]
        yield item

